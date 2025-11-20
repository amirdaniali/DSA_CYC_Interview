# accounts/views.py
from django.contrib.auth import get_user_model
from rest_framework import viewsets,  generics
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, SignupSerializer
from .permissions import IsAdminOrSelf
from rest_framework_simplejwt.views import TokenObtainPairView



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    /users endpoint:
    - Admins see all users
    - Normal users see only themselves
    - Guests denied
    """
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelf]

# accounts/views.py
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelf]

    def get_queryset(self):
        User = get_user_model()
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()   # <-- return all users
        return User.objects.filter(id=user.id)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer





class SignupView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = SignupSerializer
    permission_classes = []  # allow anyone to sign up
