from django.urls import path
from accounts.views import RegistrationView, LoginView, CustomTokenRefreshView, CustomTokenVerifyView


urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/register/', RegistrationView.as_view(), name='register'),
    path('accounts/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/token/verify/', CustomTokenVerifyView.as_view(), name='token_verify')
]
