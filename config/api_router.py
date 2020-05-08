from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from onlinefem.users.api.views import UserViewSet
from onlinefem.fem.api.views import FEMViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("fem", FEMViewSet)


app_name = "api"
urlpatterns = router.urls
