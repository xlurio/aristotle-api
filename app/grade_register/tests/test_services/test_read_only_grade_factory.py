from django.test import TestCase

from core.models import ClassroomGrade, ClassroomStudent, Grade
from core.tests.helpers import make_fake_classroom, make_fake_student
from grade_register.services import ReadOnlyGradeFactory


class ReadOnlyGradeFactoryTests(TestCase):
    """Tests for read only grade factory"""

    def test_make_grade(self) -> None:
        """Test creating a read only grade object"""
        arrangement = self._given_grade()
        result = self._when_read_only_grade_made(arrangement)
        self._then_should_create_read_only_grade(result)

    def _given_grade(self) -> Grade:
        title = "Test 1"
        grade = 91
        student = make_fake_student()
        classroom = make_fake_classroom(student)

        return Grade.objects.create(
            title=title,
            grade=grade,
            student=student,
            classroom=classroom,
        )

    def _when_read_only_grade_made(self, arrangement: Grade) -> ClassroomGrade:
        factory = ReadOnlyGradeFactory(arrangement)

        return factory.make_grade()

    def _then_should_create_read_only_grade(self, result: ClassroomGrade) -> None:
        expected_result: ClassroomGrade = ClassroomGrade.objects.get(id=result.id)
        expected_student: ClassroomStudent = expected_result.student
        expected_student_name: str = expected_student.student

        actual_student: ClassroomStudent = result.student
        actual_student_name: str = actual_student.student

        self.assertEqual(expected_student_name, actual_student_name)
