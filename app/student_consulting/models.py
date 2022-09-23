from datetime import date
from pydantic import BaseModel


class GradeDetail(BaseModel):
    """Model for reading grade details"""

    title: str
    grade: int


class ReadOnlyGrade(BaseModel):
    """Model for reading grade data"""

    classroom: str
    grades: list[GradeDetail]


class ReadOnlyAbsence(BaseModel):
    """Model for reading absence data"""

    class_room: str
    absence_amount: int
    frequency: float
    absence_dates: list[date]


class Student(BaseModel):
    """Model for reading student data"""

    student: str
    grades: list[ReadOnlyGrade]
    absences: list[ReadOnlyAbsence]
