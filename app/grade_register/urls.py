from core.routers import WriteOnlyRouter
from grade_register.api.views import GradeViewSet

router = WriteOnlyRouter()
router.register("grades", GradeViewSet, "grade")

app_name = "grades"

urlpatterns = router.urls
