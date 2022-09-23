from django.urls import path
from student_consulting.api.views import StudentView

app_name = "students"

urlpatterns = [path("", StudentView.as_view(), name="students-list")]
