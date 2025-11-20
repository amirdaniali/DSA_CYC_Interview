from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from homepage.views import SessionViewSet, SignupViewSet  

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r"sessions", SessionViewSet, basename="session")
router.register(r"signups", SignupViewSet, basename="signup")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("pages.urls")),

    
    path("api/", include(router.urls)),   # exposes /api/sessions/ and /api/signups/
    path("api-auth/", include("rest_framework.urls")),  # optional browsable login
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
