from django.urls import path
from student_consulting.api.views import StudentViewSet

app_name = "students"

urlpatterns = [path("", StudentViewSet.as_view({"get": "list"}), name="students-list")]
