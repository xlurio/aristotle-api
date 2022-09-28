from core.routers import ReadOnlyRouter
from student_consulting.api.views import StudentViewSet

router = ReadOnlyRouter()
router.register("classrooms", StudentViewSet, "classroom")

app_name = "students"

urlpatterns = router.urls
