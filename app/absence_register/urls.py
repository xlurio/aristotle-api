from django.urls import path
from absence_register.api.views import AbsenceViewSet

app_name = "absences"

urlpatterns = [
    path("", AbsenceViewSet.as_view({"post": "create"}), name="absence-list")
]
