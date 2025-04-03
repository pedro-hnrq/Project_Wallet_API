from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegistrationSerializer, LoginSerializer


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(str(user), 'test@example.com')

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class RegistrationSerializerTest(TestCase):
    def test_valid_registration(self):
        data = {
            'email': 'new@user.com',
            'password': 'validpass12',
            'first_name': 'New',
            'last_name': 'User'
        }
        serializer = RegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, 'new@user.com')

    def test_invalid_registration(self):
        data = {'email': 'invalid', 'password': 'short'}
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertIn('password', serializer.errors)


class LoginSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_valid_login(self):
        data = {'email': 'user@test.com', 'password': 'testpass123'}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        response_data = serializer.validate(data)
        self.assertIn('access_token', response_data)
        self.assertIn('user', response_data)

    def test_invalid_login(self):
        data = {'email': 'user@test.com', 'password': 'wrong'}
        serializer = LoginSerializer(data=data)
        with self.assertRaises(exceptions.AuthenticationFailed):
            serializer.validate(data)


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User'
        )
        refresh = RefreshToken.for_user(self.user)
        self.valid_token = str(refresh.access_token)

    def test_registration_view(self):
        data = {
            'email': 'new@user.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post('/api/v1/accounts/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='new@user.com').exists())

    def test_login_view(self):
        data = {'email': 'testuser@example.com', 'password': 'password123'}
        response = self.client.post('/api/v1/accounts/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    def test_invalid_login(self):
        data = {'email': 'user@test.com', 'password': 'wrong'}

        response = self.client.post('/api/v1/accounts/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

    def test_token_refresh(self):
        refresh = RefreshToken.for_user(self.user)
        data = {'refresh': str(refresh)}
        response = self.client.post('/api/v1/accounts/token/refresh/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    def test_token_verification(self):
        data = {'token': self.valid_token}
        response = self.client.post('/api/v1/accounts/token/verify/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Token Válido')

    def test_protected_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.valid_token}')
        response = self.client.get('/api/wallets/')  # Supondo que esta rota existe
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])
