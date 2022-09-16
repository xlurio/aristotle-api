from django.urls import path
from classroom_creation.api.views import ClassRoomViewSet

app_name = "classrooms"

urlpatterns = [
    path(
        "",
        ClassRoomViewSet.as_view(actions={"post": "create"}),
        name="classroom-list",
    ),
]
