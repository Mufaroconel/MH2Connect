from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, StudentAcademicHistory, SubjectCombination, Base
from database import get_db  # Assuming this is your get_db function

# Create the database engine and session
DATABASE_URL = "sqlite:///./test.db"  # Adjust the DB URL as needed
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# The function to add a student
def add_student(
    db,
    whatsapp_number: str,
    name: str = None,
    email: str = None,
    state: str = "collecting_name",
    dob: str = None,
    gender: str = None,
    address: str = None,
):
    student = Student(
        whatsapp_number=whatsapp_number,
        name=name,
        email=email,
        state=state,
        dob=dob,
        gender=gender,
        address=address,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


# Initialize the database
def initialize_db():
    # Create tables
    Base.metadata.create_all(bind=engine)


# Create a student
def create_student(phone, name, email, state, dob=None, gender=None, address=None):
    db = next(get_db())  # Get the database session
    student = add_student(db, phone, name, email, state, dob, gender, address)
    print(f"Student {student.name} created with ID {student.id}")


# Function to retrieve a student by WhatsApp number


def get_student_by_whatsapp_number(db, whatsapp_number: str):
    student = (
        db.query(Student).filter(Student.whatsapp_number == whatsapp_number).first()
    )
    if not student:
        print(f"No student found with WhatsApp number: {whatsapp_number}")
    return student


# Function to update a student's details
def update_student(
    db,
    whatsapp_number: str,
    name: str = None,
    email: str = None,
    state: str = None,
    dob: str = None,
    gender: str = None,
    address: str = None,
):
    student = (
        db.query(Student).filter(Student.whatsapp_number == whatsapp_number).first()
    )
    if not student:
        print(f"No student found with WhatsApp number: {whatsapp_number}")
        return None

    if name:
        student.name = name
    if email:
        student.email = email
    if state:
        student.state = state
    if dob:
        student.dob = dob
    if gender:
        student.gender = gender
    if address:
        student.address = address

    db.commit()
    db.refresh(student)
    print(f"Student with WhatsApp number {whatsapp_number} has been updated.")
    return student


# Function to delete a student by WhatsApp number
def delete_student(db, whatsapp_number: str):
    student = (
        db.query(Student).filter(Student.whatsapp_number == whatsapp_number).first()
    )
    if not student:
        print(f"No student found with WhatsApp number: {whatsapp_number}")
        return False

    db.delete(student)
    db.commit()
    print(f"Student with WhatsApp number {whatsapp_number} has been deleted.")
    return True


# Function to list all students
def list_all_students(db):
    students = db.query(Student).all()
    if not students:
        print("No students found.")
    else:
        print("Students List:")
        for student in students:
            print(
                f"ID: {student.id}, Name: {student.name}, WhatsApp Number: {student.whatsapp_number}, "
                f"Email: {student.email}, State: {student.state}, DOB: {student.dob}, Gender: {student.gender}, "
                f"Address: {student.address}"
            )
    return students


def save_academic_history(db, whatsapp_number, path1=None, path2=None, path3=None):
    history = StudentAcademicHistory(
        whatsapp_number=whatsapp_number, path1=path1, path2=path2, path3=path3
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


def create_academic_history(whatsapp_number, path1=None, path2=None, path3=None):
    db = next(get_db())  # Get the database session
    history = save_academic_history(db, whatsapp_number, path1, path2, path3)
    print(f"Academic history created for WhatsApp number {history.whatsapp_number}")
    return history


def get_academic_history_by_whatsapp_number(db, whatsapp_number: str):
    history = (
        db.query(StudentAcademicHistory)
        .filter(StudentAcademicHistory.whatsapp_number == whatsapp_number)
        .first()
    )
    if not history:
        print(f"No academic history found for WhatsApp number: {whatsapp_number}")
    return history

def update_academic_history(
    db,
    whatsapp_number: str,
    path1: str = None,
    path2: str = None,
    path3: str = None,
    results: str = None,
):
    """
    Updates the academic history for a student, including paths and subjects/symbols if provided.

    Args:
    db: Database session.
    whatsapp_number (str): The WhatsApp number of the student.
    path1, path2, path3 (str): File paths for the academic results images.
    results (str): A semicolon-separated string of subjects and their grades (e.g., "Maths, A; Physics, B").
    """
    # Retrieve the student's academic history based on their WhatsApp number
    history = (
        db.query(StudentAcademicHistory)
        .filter(StudentAcademicHistory.whatsapp_number == whatsapp_number)
        .first()
    )

    if not history:
        print(f"No academic history found for WhatsApp number: {whatsapp_number}")
        return None

    # Update the file paths
    if path1:
        history.path1 = path1
    if path2:
        history.path2 = path2
    if path3:
        history.path3 = path3

    # Parse the results if provided
    if results:
        # Loop through the parsed results and assign them to the appropriate subject and symbol columns
        for index, (subject, grade) in enumerate(results):
            subject_column = f"subject{index + 1}"
            symbol_column = f"symbol{index + 1}"

            if hasattr(history, subject_column) and hasattr(history, symbol_column):
                setattr(history, subject_column, subject)
                setattr(history, symbol_column, grade)

    # Commit the changes to the database
    db.commit()
    db.refresh(history)
    print(f"Academic history for WhatsApp number {whatsapp_number} has been updated.")
    return history


def delete_academic_history(db, whatsapp_number: str):
    history = (
        db.query(StudentAcademicHistory)
        .filter(StudentAcademicHistory.whatsapp_number == whatsapp_number)
        .first()
    )
    if not history:
        print(f"No academic history found for WhatsApp number: {whatsapp_number}")
        return False

    db.delete(history)
    db.commit()
    print(f"Academic history for WhatsApp number {whatsapp_number} has been deleted.")
    return True


def get_existing_academic_images(phone):
    db = next(get_db())  # Get the database session
    # Query for academic history based on WhatsApp number
    history = (
        db.query(StudentAcademicHistory)
        .filter(StudentAcademicHistory.whatsapp_number == phone)
        .first()
    )

    if not history:
        print(f"No academic history found for WhatsApp number: {phone}")
        return None

    # Return paths of the academic images
    return {"path1": history.path1, "path2": history.path2, "path3": history.path3}


def reinitialize_academic_history(
    db, whatsapp, whatsapp_number, path1="", path2="", path3=""
):
    """
    Updates the academic history record for a specific student, resetting the paths to empty strings.
    """
    try:
        # Assuming 'db' is the database session or connection
        # and the StudentAcademicHistory table has columns: 'whatsapp_number', 'path1', 'path2', 'path3'

        # Query the database to find the record by the whatsapp_number
        record = (
            db.query(StudentAcademicHistory)
            .filter(StudentAcademicHistory.whatsapp_number == whatsapp_number)
            .first()
        )

        # If the record exists, update the paths
        if record:
            record.path1 = path1
            record.path2 = path2
            record.path3 = path3
            db.commit()  # Save the changes to the database
        else:
            # If no record is found, send a notification to the user
            whatsapp.send_text(
                to=whatsapp_number,
                body="No academic history found for your account. Please upload your results first.",
            )

    except Exception as e:
        # Handle potential errors (e.g., database connection issues)
        db.rollback()  # Rollback the transaction in case of error
        whatsapp.send_text(
            to=whatsapp_number,
            body="There was an error updating your academic history. Please try again later. ⚠️",
        )
        print(f"Error: {e}")


# Function to create or update the subject combination
def create_or_update_subject_combination(
    db,
    whatsapp_number: str,
    subject1: str = None,
    subject2: str = None,
    subject3: str = None,
    subject1_option2: str = None,
    subject2_option2: str = None,
    subject3_option2: str = None,
    subject1_option3: str = None,
    subject2_option3: str = None,
    subject3_option3: str = None,
    subject_combination_state: str = None,
    suggested_subject1: str = None,
    suggested_subject2: str = None,
    suggested_subject3: str = None,
):
    # Check if the student already has a combination
    subject_combination = (
        db.query(SubjectCombination)
        .filter(SubjectCombination.whatsapp_number == whatsapp_number)
        .first()
    )

    if subject_combination:
        # Update existing combination
        if subject1:
            subject_combination.subject1 = subject1
        if subject2:
            subject_combination.subject2 = subject2
        if subject3:
            subject_combination.subject3 = subject3
        if subject1_option2:
            subject_combination.subject1_option2 = subject1_option2
        if subject2_option2:
            subject_combination.subject2_option2 = subject2_option2
        if subject3_option2:
            subject_combination.subject3_option2 = subject3_option2
        if subject1_option3:
            subject_combination.subject1_option3 = subject1_option3
        if subject2_option3:
            subject_combination.subject2_option3 = subject2_option3
        if subject3_option3:
            subject_combination.subject3_option3 = subject3_option3
        if subject_combination_state:
            subject_combination.subject_combination_state = subject_combination_state
        if suggested_subject1:
            subject_combination.suggested_subject1 = suggested_subject1
        if suggested_subject2:
            subject_combination.suggested_subject2 = suggested_subject2
        if suggested_subject3:
            subject_combination.suggested_subject3 = suggested_subject3

        db.commit()
        db.refresh(subject_combination)
        print(
            f"Subject combination for WhatsApp number {whatsapp_number} has been updated."
        )
    else:
        # Create new combination if not exists
        subject_combination = SubjectCombination(
            whatsapp_number=whatsapp_number,
            subject1=subject1,
            subject2=subject2,
            subject3=subject3,
            subject1_option2=subject1_option2,
            subject2_option2=subject2_option2,
            subject3_option2=subject3_option2,
            subject1_option3=subject1_option3,
            subject2_option3=subject2_option3,
            subject3_option3=subject3_option3,
            subject_combination_state=subject_combination_state,
            suggested_subject1=suggested_subject1,
            suggested_subject2=suggested_subject2,
            suggested_subject3=suggested_subject3,
        )
        db.add(subject_combination)
        db.commit()
        db.refresh(subject_combination)
        print(f"Subject combination created for WhatsApp number {whatsapp_number}")

    return subject_combination


# Function to get the subject combination by WhatsApp number
def get_subject_combination_by_whatsapp_number(db, whatsapp_number: str):
    subject_combination = (
        db.query(SubjectCombination)
        .filter(SubjectCombination.whatsapp_number == whatsapp_number)
        .first()
    )
    if not subject_combination:
        print(f"No subject combination found for WhatsApp number: {whatsapp_number}")
    return subject_combination


# Function to delete a subject combination
def delete_subject_combination(db, whatsapp_number: str):
    subject_combination = (
        db.query(SubjectCombination)
        .filter(SubjectCombination.whatsapp_number == whatsapp_number)
        .first()
    )
    if not subject_combination:
        print(f"No subject combination found for WhatsApp number: {whatsapp_number}")
        return False

    db.delete(subject_combination)
    db.commit()
    print(
        f"Subject combination for WhatsApp number {whatsapp_number} has been deleted."
    )
    return True


# Initialize DB (can be used for testing)
initialize_db()


def get_complete_student_info(db, whatsapp_number: str):
    """Get complete student information including academic history and subject combinations"""
    student = get_student_by_whatsapp_number(db, whatsapp_number)
    if not student:
        return None

    academic_history = get_academic_history_by_whatsapp_number(db, whatsapp_number)
    subject_combination = get_subject_combination_by_whatsapp_number(
        db, whatsapp_number
    )

    return {
        "student": student,
        "academic_history": academic_history,
        "subject_combination": subject_combination,
    }


def get_all_students_with_details(db):
    """Get all students with their complete information"""
    students = list_all_students(db)
    result = []

    for student in students:
        academic_history = get_academic_history_by_whatsapp_number(
            db, student.whatsapp_number
        )
        subject_combination = get_subject_combination_by_whatsapp_number(
            db, student.whatsapp_number
        )

        result.append(
            {
                "student": student,
                "academic_history": academic_history,
                "subject_combination": subject_combination,
            }
        )

    return result
