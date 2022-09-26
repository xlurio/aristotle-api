from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("token/", views.obtain_auth_token, name="token"),
    path("", include("user_register.urls")),
    path("", include("classroom_creation.urls")),
    path("", include("grade_register.urls")),
    path("", include("absence_register.urls")),
    path("", include("student_consulting")),
]
