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
from core.tests import helpers
from teacher_consulting.api.serializers import TeacherClassroomSerializer


def get_teacher_consulting_url(classroom_id: int | None = None) -> str:
    """Return the URL for the teacher consulting end point"""

    if classroom_id:
        return reverse("teachers:classroom-detail", kwargs={"pk": classroom_id})

    return reverse("teachers:classroom-list")


class PrivateTeacherEndpointTests(TestCase):
    """Tests for private operations on teacher consulting end point"""

    def setUp(self) -> None:
        """Runs before each test"""
        self._teacher = helpers.make_fake_teacher()
        self._client = APIClient()
        self._client.force_authenticate(self._teacher)

    def test_list(self) -> None:
        """Test displaying all teacher data"""
        self._given_data()
        result = self._when_get_request()
        self._then_should_display_all_data(result)

    def _given_data(self) -> None:
        student1 = helpers.make_fake_student(first_name="Elton")
        student2 = helpers.make_fake_student(first_name="Tahani")
        classroom1: ClassRoom = helpers.make_fake_classroom(student1)
        classroom1.members.add(self._teacher)
        grade1: Grade = helpers.make_fake_grade(student1, classroom=classroom1)

        classroom2: ClassRoom = helpers.make_fake_classroom(student2, subject="physics")
        classroom2.members.add(self._teacher)
        grade2: Grade = helpers.make_fake_grade(
            student2, classroom=classroom2, grade=82
        )
        absence: Absence = helpers.make_fake_absence(student2, classroom=classroom2)

        student_classroom1: StudentClassroom = helpers.make_fake_student_classroom(
            student1, classroom1
        )
        student_classroom2: StudentClassroom = helpers.make_fake_student_classroom(
            student2, classroom2
        )

        teacher_classroom1: TeacherClassroom = helpers.make_fake_teacher_classroom(
            classroom1
        )
        teacher_classroom2: TeacherClassroom = helpers.make_fake_teacher_classroom(
            classroom2
        )

        classroom1_student: ClassroomStudent = helpers.make_fake_classroom_student(
            student1, teacher_classroom1
        )
        classroom2_student: ClassroomStudent = helpers.make_fake_classroom_student(
            student2, teacher_classroom2
        )

        classroom_grade1: ClassroomGrade = helpers.make_fake_classroom_grade(
            student_classroom1, classroom1_student
        )
        classroom_grade2: ClassroomGrade = helpers.make_fake_classroom_grade(
            student_classroom2, classroom2_student
        )

        helpers.make_fake_grade_detail(grade1, classroom_grade1)
        helpers.make_fake_grade_detail(grade2, classroom_grade2)

        classroom_absence: ClassroomAbsence = helpers.make_fake_classroom_absence(
            student_classroom2, classroom2_student
        )
        helpers.make_fake_absence_detail(absence, classroom_absence)

    def _when_get_request(self) -> Any:
        url = get_teacher_consulting_url()

        return self._client.get(url)

    def _then_should_display_all_data(self, result: Any) -> None:
        expected_status_code = status.HTTP_200_OK

        classrooms: QuerySet[ClassRoom] = ClassRoom.objects.filter(
            members__id=self._teacher.id
        )
        classrooms_id: list[int] = [classroom.id for classroom in classrooms]
        teacher_classrooms: QuerySet[TeacherClassroom]
        teacher_classrooms = TeacherClassroom.objects.filter(
            classroom_id__in=classrooms_id
        )
        teacher_classrooms = teacher_classrooms.order_by("id")
        serializer = TeacherClassroomSerializer(teacher_classrooms, many=True)
        expected_serialized_data = serializer.data

        self.assertEqual(expected_status_code, result.status_code)
        self.assertEqual(expected_serialized_data, result.data)

    def test_retrieve(self) -> None:
        """Test retrieve data from a specific class room"""
        arrangement = self._given_classroom_id()
        result = self._when_id_get_requested(arrangement)
        self._then_should_retrieve_classroom(arrangement, result)

    def _given_classroom_id(self) -> int:
        student1 = helpers.make_fake_student(first_name="Elton")
        student2 = helpers.make_fake_student(first_name="Tahani")

        classroom: ClassRoom = helpers.make_fake_classroom(student1)
        classroom.members.add(self._teacher, student2)

        grade1: Grade = helpers.make_fake_grade(student1, classroom=classroom)
        grade2: Grade = helpers.make_fake_grade(student2, classroom=classroom, grade=82)
        absence: Absence = helpers.make_fake_absence(student2, classroom=classroom)

        student_classroom1: StudentClassroom = helpers.make_fake_student_classroom(
            student1, classroom
        )
        student_classroom2: StudentClassroom = helpers.make_fake_student_classroom(
            student2, classroom
        )

        teacher_classroom: TeacherClassroom = helpers.make_fake_teacher_classroom(
            classroom
        )

        classroom1_student: ClassroomStudent = helpers.make_fake_classroom_student(
            student1, teacher_classroom
        )
        classroom2_student: ClassroomStudent = helpers.make_fake_classroom_student(
            student2, teacher_classroom
        )

        classroom_grade1: ClassroomGrade = helpers.make_fake_classroom_grade(
            student_classroom1, classroom1_student
        )
        classroom_grade2: ClassroomGrade = helpers.make_fake_classroom_grade(
            student_classroom2, classroom2_student
        )

        helpers.make_fake_grade_detail(grade1, classroom_grade1)
        helpers.make_fake_grade_detail(grade2, classroom_grade2)

        classroom_absence: ClassroomAbsence = helpers.make_fake_classroom_absence(
            student_classroom2, classroom2_student
        )
        helpers.make_fake_absence_detail(absence, classroom_absence)

        return teacher_classroom.id

    def _when_id_get_requested(self, arrangement: int) -> Any:
        url = get_teacher_consulting_url(arrangement)

        return self._client.get(url)

    def _then_should_retrieve_classroom(self, arrangement: int, result: Any) -> None:
        expected_status_code = status.HTTP_200_OK

        classroom = TeacherClassroom.objects.get(id=arrangement)
        serializer = TeacherClassroomSerializer(classroom)
        expected_serialized_data = serializer.data

        self.assertEqual(expected_status_code, result.status_code)
        self.assertEqual(expected_serialized_data, result.data)
