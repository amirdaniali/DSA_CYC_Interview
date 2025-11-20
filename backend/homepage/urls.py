from django.urls import path, include
from rest_framework import routers
from .views import SessionViewSet, SignupViewSet

router = routers.DefaultRouter()
router.register(r"sessions", SessionViewSet, basename="session")
router.register(r"signups", SignupViewSet, basename="signup")

urlpatterns = [
    path("", include(router.urls)),
]
