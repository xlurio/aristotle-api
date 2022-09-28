from typing import Any

from django.db.models.query import QuerySet
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Absence,
    ClassRoom,
    ClassroomAbsence,
    ClassroomGrade,
    ClassroomStudent,
    Grade,
    StudentClassroom,
    TeacherClassroom,
)
from core.tests.helpers import (
    make_fake_absence,
    make_fake_absence_detail,
    make_fake_classroom,
    make_fake_classroom_absence,
    make_fake_classroom_grade,
    make_fake_classroom_student,
    make_fake_grade,
    make_fake_grade_detail,
    make_fake_student,
    make_fake_student_classroom,
    make_fake_teacher_classroom,
)
from student_consulting.api.serializers import StudentClassroomSerializer


def get_student_consulting_url(classroom_id: int | None = None) -> str:
    """Returns the student consulting URL"""

    if classroom_id:
        return reverse("students:classroom-detail", kwargs={"pk": classroom_id})

    return reverse("students:classroom-list")


class PrivateStudentEndpointTests(TestCase):
    """Tests for the private operations on student end point"""

    def setUp(self) -> None:
        """Runs before each test"""
        self._student = make_fake_student()
        self._client = APIClient()

        self._client.force_authenticate(self._student)

    def test_list(self) -> None:
        """Test listing students data"""
        self._given_student_data()
        result = self._when_get_requested()
        self._then_should_display_student_data(result)

    def _given_student_data(self) -> None:
        classroom1: ClassRoom = make_fake_classroom(self._student)
        grade1: Grade = make_fake_grade(self._student, classroom=classroom1)

        classroom2: ClassRoom = make_fake_classroom(self._student, subject="physics")
        grade2: Grade = make_fake_grade(self._student, classroom=classroom2, grade=82)
        absence: Absence = make_fake_absence(self._student, classroom=classroom2)

        student_classroom1: StudentClassroom = make_fake_student_classroom(
            self._student, classroom1
        )
        student_classroom2: StudentClassroom = make_fake_student_classroom(
            self._student, classroom2
        )

        teacher_classroom1: TeacherClassroom = make_fake_teacher_classroom(classroom1)
        teacher_classroom2: TeacherClassroom = make_fake_teacher_classroom(classroom2)

        classroom1_student: ClassroomStudent = make_fake_classroom_student(
            self._student, teacher_classroom1
        )
        classroom2_student: ClassroomStudent = make_fake_classroom_student(
            self._student, teacher_classroom2
        )

        classroom_grade1: ClassroomGrade = make_fake_classroom_grade(
            student_classroom1, classroom1_student
        )
        classroom_grade2: ClassroomGrade = make_fake_classroom_grade(
            student_classroom2, classroom2_student
        )

        make_fake_grade_detail(grade1, classroom_grade1)
        make_fake_grade_detail(grade2, classroom_grade2)

        classroom_absence: ClassroomAbsence = make_fake_classroom_absence(
            student_classroom2, classroom2_student
        )
        make_fake_absence_detail(absence, classroom_absence)

    def _when_get_requested(self) -> Any:
        url = get_student_consulting_url()
        return self._client.get(url)

    def _then_should_display_student_data(self, result: Any) -> None:
        expected_status_code = status.HTTP_200_OK

        expected_classrooms: QuerySet[
            StudentClassroom
        ] = StudentClassroom.objects.filter(user_id=self._student.id)
        expected_classrooms = expected_classrooms.order_by("id")
        serializer = StudentClassroomSerializer(expected_classrooms, many=True)
        expected_serialized_data = serializer.data

        self.assertEqual(expected_status_code, result.status_code)
        self.assertEqual(expected_serialized_data, result.data)

    def test_retrieve(self) -> None:
        """Test retriving class room"""
        arrangement = self._given_classroom_id()
        result = self._when_get_request_with_id(arrangement)
        self._then_should_retrieve_specific_classroom(arrangement, result)

    def _given_classroom_id(self) -> int:
        classroom: ClassRoom = make_fake_classroom(self._student)
        grade: Grade = make_fake_grade(self._student, classroom=classroom)

        student_classroom: StudentClassroom = make_fake_student_classroom(
            self._student, classroom
        )
        teacher_classroom: TeacherClassroom = make_fake_teacher_classroom(classroom)
        classroom_student: ClassroomStudent = make_fake_classroom_student(
            self._student, teacher_classroom
        )

        classroom_grade: ClassroomGrade = make_fake_classroom_grade(
            student_classroom, classroom_student
        )
        make_fake_grade_detail(grade, classroom_grade)

        return student_classroom.id

    def _when_get_request_with_id(self, arrangement: int) -> Any:
        url = get_student_consulting_url(arrangement)

        return self._client.get(url)

    def _then_should_retrieve_specific_classroom(
        self, arrangement: int, result: Any
    ) -> None:
        expected_status_code = status.HTTP_200_OK

        expected_classroom = StudentClassroom.objects.get(id=arrangement)
        serializer = StudentClassroomSerializer(expected_classroom)
        expected_serialized_data = serializer.data

        self.assertEqual(expected_status_code, result.status_code)
        self.assertEqual(expected_serialized_data, result.data)
