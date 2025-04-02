from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .serializers import LoginSerializer, RegistrationSerializer, CustomTokenRefreshSerializer, CustomTokenVerifySerializer
from drf_spectacular.utils import extend_schema
from rest_framework import generics


@extend_schema(tags=['Accounts'], description='Autentica um usuário e retorna um token de acesso.')
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


@extend_schema(tags=['Accounts'], description='Registra um novo usuário.')
class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    authentication_classes = []
    permission_classes = []


@extend_schema(tags=['Accounts'], description='Verifica a validade de um token de acesso.')
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


@extend_schema(tags=['Accounts'], description='Verifica a validade de um token de acesso.')
class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer
