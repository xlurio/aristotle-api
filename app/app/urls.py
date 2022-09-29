from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken import views

urlpatterns = [
    path("token/", views.obtain_auth_token, name="token"),
    path("", include("user_register.urls")),
    path("", include("classroom_creation.urls")),
    path("", include("grade_register.urls")),
    path("", include("absence_register.urls")),
    path("student/", include("student_consulting.urls")),
    path("teacher/", include("teacher_consulting.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
