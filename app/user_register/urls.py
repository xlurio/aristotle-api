from core.routers import WriteOnlyRouter
from user_register.api.views import UserViewSet

router = WriteOnlyRouter()
router.register("users", UserViewSet, "user")

app_name = "users"

urlpatterns = router.urls
