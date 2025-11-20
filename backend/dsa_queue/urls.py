from django.urls import path, include
from rest_framework import routers
from .views import SessionViewSet, SignupViewSet, EventTemplateViewSet, InterviewQueueViewSet

router = routers.DefaultRouter()
router.register(r"sessions", SessionViewSet, basename="session")
router.register(r"signups", SignupViewSet, basename="signup")
router.register(r"templates", EventTemplateViewSet, basename="template")
router.register(r"queue", InterviewQueueViewSet, basename="queue")

urlpatterns = [
    path("", include(router.urls)),
]
