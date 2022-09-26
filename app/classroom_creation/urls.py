from core.routers import WriteOnlyRouter
from classroom_creation.api.views import ClassRoomViewSet

router = WriteOnlyRouter()
router.register("classrooms", ClassRoomViewSet, "classroom")

app_name = "classrooms"

urlpatterns = router.urls
