from datetime import date
from pydantic import BaseModel


class GradeDetail(BaseModel):
    """Model for reading grade details"""

    title: str
    grade: int


class ReadOnlyGrade(BaseModel):
    """Model for reading grade data"""

    classroom: str
    average: float
    grades: list[GradeDetail]


class ReadOnlyAbsence(BaseModel):
    """Model for reading absence data"""

    class_room: str
    absence_amount: int
    frequency: float
    absence_dates: list[date]


class StudentDetail(BaseModel):
    """Model for reading the detailed data of a student"""

    student: str
    grades: list[ReadOnlyGrade]
    absences: list[ReadOnlyAbsence]


class Student(BaseModel):
    """Model for reading students from class data"""

    student_id: int
    name: str


class ClassRoomDetails(BaseModel):
    """Model for reading the detailed data of a class room"""

    subject: str
    students: list[Student]


class ReadOnlyClassroom(BaseModel):
    """Models for reading the teacher classrooms data"""

    classroom_id: int
    name: str


class Teacher(BaseModel):
    """Model for reading the teacher data"""

    teacher: str
    classrooms: list[ReadOnlyClassroom]
