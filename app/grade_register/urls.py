from django.urls import path
from grade_register.api.views import GradeViewSet

app_name = "grades"

urlpatterns = [path("", GradeViewSet.as_view({"post": "create"}), name="grade-list")]
