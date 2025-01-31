from sqlalchemy.orm import Session
from models import Student, Base


def create_student(db: Session, whatsapp_number: str):
    """
    Create a new student record with the given WhatsApp number.
    """
    db_student = Student(whatsapp_number=whatsapp_number)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student_field(db: Session, whatsapp_number: str, field: str, value: str):
    """
    Update a specific field for the student identified by the WhatsApp number.
    """
    student = db.query(Student).filter(Student.whatsapp_number == whatsapp_number).first()
    if student:
        setattr(student, field, value)
        db.commit()
        db.refresh(student)
    return student


def get_student_by_id(db: Session, student_id: int):
    """
    Retrieve a student record by its ID.
    """
    return db.query(Student).filter(Student.id == student_id).first()


def get_student_by_whatsapp_number(db: Session, whatsapp_number: str):
    """
    Retrieve a student record by its WhatsApp number.
    """
    return db.query(Student).filter(Student.whatsapp_number == whatsapp_number).first()

phone = "1234567890"