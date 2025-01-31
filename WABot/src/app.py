import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from fastapi.staticfiles import StaticFiles

from whatsapp_config import whatsapp
from wa_cloud_py.messages.types import (
    TextMessage,
    ImageMessage,
    DocumentMessage,
    AudioMessage,
    VideoMessage,
    LocationMessage,
    InteractiveListMessage,
)
from database import get_db
from db_operations import (
    get_student_by_whatsapp_number,
    create_student,
    update_student,
    create_academic_history,
    delete_academic_history,
    create_or_update_subject_combination,
    update_academic_history,
    get_academic_history_by_whatsapp_number,
    get_all_students_with_details,
    get_complete_student_info,
)
from messages.option_messages import (
    send_welcome_message,
    enrollment_welcome_message,
    get_student_fullname,
    get_student_birth,
    get_student_address,
    get_olevel_results,
    get_student_gender,
    reupload_olevel_results,
    request_preferred_combination,
    request_second_combination,
    request_third_combination,
    confirm_combination,
    edit_combination_message,
    information_confirmation_message,
    lower_six_application_success_message,
    get_olevel_results_by_subject,
)
from validation.personal_details_validation import convert_to_datetime
from other_operations import handle_image_upload
from subject_combination_validator import (
    validate_combination,
    separate_combination,
    parse_academic_results,
)
from models import User, StudentAcademicHistory, SubjectCombination, Student

load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

if not VERIFY_TOKEN:
    raise ValueError("VERIFY_TOKEN environment variable is not set")
if not ACCESS_TOKEN:
    raise ValueError("ACCESS_TOKEN environment variable is not set")
if not PHONE_NUMBER_ID:
    raise ValueError("PHONE_NUMBER_ID environment variable is not set")

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Your JWT secret and algorithm
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserCreate(BaseModel):
    username: str
    password: str


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return "complete"


@app.get("/test")
async def test_connection():
    return {"message": "Connection successful!"}


@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)


# Authenticate the user
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


# Create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token is invalid or expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Token is invalid or expired")


@app.get("/verify-token/{token}")
async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message": "Token is valid"}


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if token and token == VERIFY_TOKEN:
        return PlainTextResponse(content=challenge)

    raise HTTPException(status_code=403, detail="Invalid verify token")


@app.post("/webhook")
async def receive_message(request: Request):
    try:
        body = await request.body()
        message = whatsapp.parse(body)
        phone = message.user.phone_number
        username = message.user.name
        db = next(get_db())
        student_state = None
        student = get_student_by_whatsapp_number(db=db, whatsapp_number=phone)
        if student:
            student_state = student.state
            print(f"student with state {student_state} found")
        else:
            create_student(phone=phone, state="none", email=None, name=None)
            print("student not found")
        if isinstance(message, TextMessage):
            if student_state == "none":
                send_welcome_message(whatsapp, phone, username)
            elif student_state == "collecting_name":
                get_student_birth(whatsapp, phone)
                name = message.body
                update_student(
                    db=db, whatsapp_number=phone, name=name, state="collecting_dob"
                )
            elif student_state == "collecting_dob":
                get_student_gender(whatsapp, phone)
                dob = message.body
                dob = convert_to_datetime(dob)
                update_student(
                    db=db,
                    whatsapp_number=phone,
                    dob=dob,
                    state="collecting_gender",
                )
            elif student_state == "collecting_gender":
                get_student_address(whatsapp, phone)
                gender = message.body
                update_student(
                    db=db,
                    whatsapp_number=phone,
                    gender=gender,
                    state="collecting_address",
                )
                pass
            elif student_state == "collecting_address":
                get_olevel_results_by_subject(whatsapp, phone)
                address = message.body
                update_student(
                    db=db,
                    whatsapp_number=phone,
                    address=address,
                    state="collecting_academics",
                )
            elif student_state == "collecting_academics":
                results_str = message.body
                print("passing academic history")
                results = parse_academic_results(results_str)
                print(results)
                academic_history = get_academic_history_by_whatsapp_number(
                    db=db, whatsapp_number=phone
                )
                if academic_history:
                    update_academic_history(
                        db=db, whatsapp_number=phone, results=results
                    )
                    get_olevel_results(whatsapp, phone)
                    update_student(db=db, whatsapp_number=phone, state="upload_photo")
                else:
                    create_academic_history(whatsapp_number=phone)
                    update_academic_history(
                        db=db, whatsapp_number=phone, results=results
                    )
                    get_olevel_results(whatsapp, phone)
                    update_student(db=db, whatsapp_number=phone, state="upload_photo")
            elif student_state == "collecting_combination":
                combination = message.body
                validate_comb = validate_combination(combination)
                print("validating combination")
                if validate_comb:
                    print("separating subjects")
                    Subject1, Subject2, Subject3 = separate_combination(combination)
                    request_second_combination(whatsapp, phone)
                    create_or_update_subject_combination(
                        db=db,
                        whatsapp_number=phone,
                        subject1=Subject1,
                        subject2=Subject2,
                        subject3=Subject3,
                    )
                    update_student(
                        db=db, whatsapp_number=phone, state="collecting_combination_2"
                    )
            elif student_state == "collecting_combination_2":
                combination = message.body
                validate_comb = validate_combination(combination)
                print("validating combination")
                if validate_comb:
                    print("separating subjects")
                    Subject1, Subject2, Subject3 = separate_combination(combination)
                    request_third_combination(whatsapp, phone)
                    create_or_update_subject_combination(
                        db=db,
                        whatsapp_number=phone,
                        subject1_option2=Subject1,
                        subject2_option2=Subject2,
                        subject3_option2=Subject3,
                    )
                update_student(
                    db=db, whatsapp_number=phone, state="collecting_combination_3"
                )
            elif student_state == "collecting_combination_3":
                combination = message.body
                validate_comb = validate_combination(combination)
                print("validating combination")
                if validate_comb:
                    print("separating subjects")
                    Subject1, Subject2, Subject3 = separate_combination(combination)
                    confirm_combination(whatsapp, phone)
                    create_or_update_subject_combination(
                        db=db,
                        whatsapp_number=phone,
                        subject1_option3=Subject1,
                        subject2_option3=Subject2,
                        subject3_option3=Subject3,
                    )
                update_student(db=db, whatsapp_number=phone, state="verify_combination")
            elif student_state == "editing_combination_1":
                combination = message.body
                validate_comb = validate_combination(combination)
                print("validating combination")
                if validate_comb:
                    print("separating subjects")
                    Subject1, Subject2, Subject3 = separate_combination(combination)
                    confirm_combination(whatsapp, phone)
                    create_or_update_subject_combination(
                        db=db,
                        whatsapp_number=phone,
                        subject1=Subject1,
                        subject2=Subject2,
                        subject3=Subject3,
                    )
                    update_student(
                        db=db, whatsapp_number=phone, state="verify_combination"
                    )
            elif student_state == "editing_combination_2":
                combination = message.body
                validate_comb = validate_combination(combination)
                print("validating combination")
                if validate_comb:
                    print("separating subjects")
                    Subject1, Subject2, Subject3 = separate_combination(combination)
                    confirm_combination(whatsapp, phone)
                    create_or_update_subject_combination(
                        db=db,
                        whatsapp_number=phone,
                        subject1_option2=Subject1,
                        subject2_option2=Subject2,
                        subject3_option2=Subject3,
                    )
                    update_student(
                        db=db, whatsapp_number=phone, state="verify_combination"
                    )
            elif student_state == "editing_combination_3":
                combination = message.body
                validate_comb = validate_combination(combination)
                print("validating combination")
                if validate_comb:
                    print("separating subjects")
                    Subject1, Subject2, Subject3 = separate_combination(combination)
                    confirm_combination(whatsapp, phone)
                    create_or_update_subject_combination(
                        db=db,
                        whatsapp_number=phone,
                        subject1_option2=Subject1,
                        subject2_option2=Subject2,
                        subject3_option2=Subject3,
                    )
                    update_student(
                        db=db, whatsapp_number=phone, state="verify_combination"
                    )
        if isinstance(message, ImageMessage):
            print("handling image message")
            handle_image_upload(db, whatsapp, phone, message, student_state)
        elif isinstance(message, DocumentMessage):
            print(f"Received document: {message.filename}")
        elif isinstance(message, AudioMessage):
            print(f"Received audio. Voice note: {message.is_voice}")
        elif isinstance(message, VideoMessage):
            print("Received video")
        elif isinstance(message, LocationMessage):
            print(f"Received location: {message.latitude}, {message.longitude}")
        elif isinstance(message, InteractiveListMessage):
            user_choice = message.reply_id
            if user_choice == "class_enrollment":
                result = enrollment_welcome_message(whatsapp, phone)
                if result:
                    message_sent, res = result
            elif user_choice == "form_1":
                pass
            elif user_choice == "lower_six":
                student = get_student_by_whatsapp_number(db=db, whatsapp_number=phone)
                student_state = student.state
                if student_state == "none":
                    get_student_fullname(whatsapp, phone)
                    update_student(
                        db=db, whatsapp_number=phone, state="collecting_name"
                    )
            elif user_choice == "review_images":
                pass
            elif user_choice == "reupload_images":
                delete_academic_history(db=db, whatsapp_number=phone)
                create_academic_history(whatsapp_number=phone)
                reupload_olevel_results(whatsapp, phone)
            elif user_choice == "continue_application":
                update_student(
                    db=db, whatsapp_number=phone, state="collecting_combination"
                )
                request_preferred_combination(whatsapp, phone)
            elif user_choice == "confirm_combination":
                information_confirmation_message(whatsapp, phone)
            elif user_choice == "edit_combination":
                edit_combination_message(whatsapp, phone)
            elif user_choice == "edit_option_A":
                update_student(
                    db=db, whatsapp_number=phone, state="editing_combination_1"
                )
                request_preferred_combination(whatsapp, phone)
            elif user_choice == "edit_option_B":
                update_student(
                    db=db, whatsapp_number=phone, state="editing_combination_2"
                )
                request_second_combination(whatsapp, phone)
            elif user_choice == "edit_option_C":
                update_student(
                    db=db, whatsapp_number=phone, state="editing_combination_3"
                )
                request_third_combination(whatsapp, phone)
            elif user_choice == "confirm_accuracy":
                lower_six_application_success_message(whatsapp, phone, username)
                update_student(db=db, whatsapp_number=phone, state="none")
            elif user_choice == "tuition_fees":
                pass
            elif user_choice == "school_schedule":
                pass
            elif user_choice == "other_options":
                pass
        return {"status": "processed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/students")
async def get_students(db: Session = Depends(get_db)):
    students = get_all_students_with_details(db)
    return students


@app.get("/api/students/{whatsapp_number}")
async def get_student(whatsapp_number: str, db: Session = Depends(get_db)):
    student = get_complete_student_info(db, whatsapp_number)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.put("/api/students/{whatsapp_number}/state")
async def update_student_state(
    whatsapp_number: str, state: dict, db: Session = Depends(get_db)
):
    # Add your state update logic here
    pass


@app.put("/api/students/{whatsapp_number}/subject-combination-state")
async def update_subject_combination_state(
    whatsapp_number: str, state: dict, db: Session = Depends(get_db)
):
    # Add your subject combination state update logic here
    pass


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )


@app.get("/protected-route")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user.username}!"}


class DashboardStats(BaseModel):
    total_students: int
    pending_registrations: int
    pending_combinations: int
    total_academic_records: int
    students_by_state: Dict[str, int]
    recent_students: List[Dict[str, str]]
    subject_combinations_stats: Dict[str, int]
    academic_performance: Dict[str, int]


# Utility function to get counts based on conditions
def get_count(db: Session, model, filter_by=None):
    query = db.query(model)
    if filter_by:
        query = query.filter(filter_by)
    return query.count()


# Utility function for grouping data
def get_grouped_data(db: Session, model, group_by, count_field):
    return dict(db.query(group_by, func.count(count_field)).group_by(group_by).all())


@app.get("/api/dashboard", response_model=DashboardStats)
async def get_dashboard_data(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    # Fetch all necessary counts and data
    total_students = get_count(db, Student)
    pending_registrations = get_count(db, Student, Student.state == "collecting_name")
    pending_combinations = get_count(
        db,
        SubjectCombination,
        SubjectCombination.subject_combination_state == "Pending",
    )
    total_academic_records = get_count(db, StudentAcademicHistory)
    students_by_state = get_grouped_data(db, Student, Student.state, Student.id)

    # Fetch recent students
    recent_students = [
        {
            "name": student.name or "Pending",
            "whatsapp_number": student.whatsapp_number,
            "state": student.state,
        }
        for student in db.query(Student).order_by(desc(Student.id)).limit(5).all()
    ]

    # Fetch subject combinations stats
    subject_combinations_stats = get_grouped_data(
        db,
        SubjectCombination,
        SubjectCombination.subject_combination_state,
        SubjectCombination.id,
    )

    # Calculate academic performance
    academic_records = db.query(StudentAcademicHistory).all()
    performance_stats = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}
    for record in academic_records:
        symbols = [
            getattr(record, f"symbol{i}")
            for i in range(1, 15)
            if getattr(record, f"symbol{i}")
        ]
        for symbol in symbols:
            if symbol:
                performance_stats[symbol[0]] += 1

    return DashboardStats(
        total_students=total_students,
        pending_registrations=pending_registrations,
        pending_combinations=pending_combinations,
        total_academic_records=total_academic_records,
        students_by_state=students_by_state,
        recent_students=recent_students,
        subject_combinations_stats=subject_combinations_stats,
        academic_performance=performance_stats,
    )


@app.get("/api/dashboard/students/{whatsapp_number}")
async def get_student_details(
    whatsapp_number: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Fetch the student record
    student = (
        db.query(Student).filter(Student.whatsapp_number == whatsapp_number).first()
    )
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Fetch academic history and subject combination
    academic_history = (
        db.query(StudentAcademicHistory)
        .filter(StudentAcademicHistory.whatsapp_number == whatsapp_number)
        .first()
    )
    subject_combination = (
        db.query(SubjectCombination)
        .filter(SubjectCombination.whatsapp_number == whatsapp_number)
        .first()
    )

    return {
        "student": {
            "name": student.name,
            "whatsapp_number": student.whatsapp_number,
            "email": student.email,
            "state": student.state,
            "dob": student.dob,
            "gender": student.gender,
            "address": student.address,
        },
        "academic_history": academic_history,
        "subject_combination": subject_combination,
    }
