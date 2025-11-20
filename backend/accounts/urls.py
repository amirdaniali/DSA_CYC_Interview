# accounts/urls.py
from rest_framework.routers import DefaultRouter
from accounts.views import SignupView, UserViewSet, CustomTokenObtainPairView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
