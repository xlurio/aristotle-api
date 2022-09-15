from django.urls import path
from user_register.api.views import UserViewSet

app_name = "users"

urlpatterns = [
    path("", UserViewSet.as_view(actions={"post": "create"}), name="user-list"),
]
