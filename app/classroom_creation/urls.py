from classroom_creation.api.views import ClassRoomViewSet
from core.routers import WriteOnlyRouter

router = WriteOnlyRouter()
router.register("classrooms", ClassRoomViewSet, "classroom")

app_name = "classrooms"

urlpatterns = router.urls
