from core.routers import ReadOnlyRouter
from teacher_consulting.api.views import TeacherViewSet

router = ReadOnlyRouter()
router.register("classrooms", TeacherViewSet, "classroom")

app_name = "teacher"

urlpatterns = router.urls
