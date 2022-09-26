from absence_register.api.views import AbsenceViewSet
from core.routers import WriteOnlyRouter

router = WriteOnlyRouter()
router.register(r"absences", AbsenceViewSet, "absence")

app_name = "absences"

urlpatterns = router.urls
