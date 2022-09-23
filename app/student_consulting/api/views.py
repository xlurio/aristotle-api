from typing import Any
from rest_framework import views, authentication, request, response
from student_consulting.services import StudentDataFactory
from student_consulting.models import Student
from student_consulting.permissions import IsStudent
from student_consulting.api.serializers import StudentSerializer
from core import models


class StudentView(views.APIView):
    """Student data view"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsStudent]

    def get(self, request: request.Request, format=None):
        """Display all student data"""
        student_instance: models.User = request.user

        factory: StudentDataFactory = StudentDataFactory()
        student_data: dict[str, Any] = factory.make_data(student_instance)

        return response.Response(student_data)
