from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    whatsapp_number = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    state = Column(String, default="collecting_name")
    dob = Column(Date, nullable=True)  # Date of Birth
    gender = Column(String, nullable=True)  # Gender
    address = Column(String, nullable=True)  # Address


class StudentAcademicHistory(Base):
    __tablename__ = "student_academic_history"

    id = Column(Integer, primary_key=True, index=True)
    whatsapp_number = Column(
        String, nullable=False, index=True, unique=True
    )  # Link to student via WhatsApp number
    path1 = Column(String, nullable=True)
    path2 = Column(String, nullable=True)
    path3 = Column(String, nullable=True)
    subject1 = Column(String, nullable=True)
    symbol1 = Column(String, nullable=True)
    subject2 = Column(String, nullable=True)
    symbol2 = Column(String, nullable=True)
    subject3 = Column(String, nullable=True)
    symbol3 = Column(String, nullable=True)
    subject4 = Column(String, nullable=True)
    symbol4 = Column(String, nullable=True)
    subject5 = Column(String, nullable=True)
    symbol5 = Column(String, nullable=True)
    subject6 = Column(String, nullable=True)
    symbol6 = Column(String, nullable=True)
    subject7 = Column(String, nullable=True)
    symbol7 = Column(String, nullable=True)
    subject8 = Column(String, nullable=True)
    symbol8 = Column(String, nullable=True)
    subject9 = Column(String, nullable=True)
    symbol9 = Column(String, nullable=True)
    subject10 = Column(String, nullable=True)
    symbol10 = Column(String, nullable=True)
    subject11 = Column(String, nullable=True)
    symbol11 = Column(String, nullable=True)
    subject12 = Column(String, nullable=True)
    symbol12 = Column(String, nullable=True)
    subject13 = Column(String, nullable=True)
    symbol13 = Column(String, nullable=True)
    subject14 = Column(String, nullable=True)
    symbol14 = Column(String, nullable=True)


class SubjectCombination(Base):
    __tablename__ = "subject_combination"

    id = Column(Integer, primary_key=True, index=True)
    whatsapp_number = Column(
        String, nullable=False, index=True, unique=True
    )  # Link to student via WhatsApp number

    subject1 = Column(String, nullable=True)
    subject2 = Column(String, nullable=True)
    subject3 = Column(String, nullable=True)

    # 2nd and 3rd combination options
    subject1_option2 = Column(String, nullable=True)
    subject2_option2 = Column(String, nullable=True)
    subject3_option2 = Column(String, nullable=True)

    subject1_option3 = Column(String, nullable=True)
    subject2_option3 = Column(String, nullable=True)
    subject3_option3 = Column(String, nullable=True)

    # New field to track the combination state (e.g., accepted, rejected, etc.)
    subject_combination_state = Column(
        String, nullable=True
    )  # Could be "Accepted", "Rejected", "Suggested"

    # New fields to store suggested combinations by the school
    suggested_subject1 = Column(String, nullable=True)
    suggested_subject2 = Column(String, nullable=True)
    suggested_subject3 = Column(String, nullable=True)
