from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from decimal import Decimal
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer


class WalletModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@test.com', password='password')

    def test_create_wallet(self):
        wallet = Wallet.objects.create(user=self.user, balance=Decimal('100.00'))
        self.assertEqual(wallet.balance, Decimal('100.00'))
        self.assertEqual(wallet.user.email, 'user@test.com')


class TransactionModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@test.com', password='pass')
        self.user2 = User.objects.create_user(email='user2@test.com', password='pass')
        self.wallet1 = Wallet.objects.create(user=self.user1, balance=Decimal('100.00'))
        self.wallet2 = Wallet.objects.create(user=self.user2, balance=Decimal('50.00'))

    def test_create_transaction(self):
        transaction = Transaction.objects.create(
            sender_wallet=self.wallet1,
            receiver_wallet=self.wallet2,
            amount=Decimal('30.00'),
            status='completed'
        )
        self.assertEqual(transaction.amount, Decimal('30.00'))
        self.assertEqual(transaction.status, 'completed')

    def test_sender_receiver_same_validation(self):
        transaction = Transaction(
            sender_wallet=self.wallet1,
            receiver_wallet=self.wallet1,
            amount=Decimal('10.00'),
            status='completed'
        )
        with self.assertRaises(ValidationError):
            transaction.full_clean()

    def test_amount_positive_validation(self):
        transaction = Transaction(
            sender_wallet=self.wallet1,
            receiver_wallet=self.wallet2,
            amount=Decimal('-10.00'),
            status='completed'
        )
        with self.assertRaises(ValidationError):
            transaction.full_clean()


class WalletSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@test.com', password='password')
        self.wallet = Wallet.objects.create(user=self.user, balance=Decimal('100.00'))

    def test_wallet_serializer(self):
        serializer = WalletSerializer(self.wallet)
        self.assertEqual(serializer.data['user_email'], 'user@test.com')
        self.assertEqual(serializer.data['balance'], '100.00')


class TransactionSerializerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@test.com', password='pass')
        self.user2 = User.objects.create_user(email='user2@test.com', password='pass')
        self.wallet1 = Wallet.objects.create(user=self.user1, balance=Decimal('100.00'))
        self.wallet2 = Wallet.objects.create(user=self.user2, balance=Decimal('50.00'))
        self.transaction = Transaction.objects.create(
            sender_wallet=self.wallet1,
            receiver_wallet=self.wallet2,
            amount=Decimal('30.00'),
            status='completed'
        )

    def test_transaction_serializer(self):
        serializer = TransactionSerializer(self.transaction)
        self.assertEqual(serializer.data['sender_email'], 'user1@test.com')
        self.assertEqual(serializer.data['receiver_email'], 'user2@test.com')
        self.assertEqual(serializer.data['amount'], '30.00')


class WalletViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='password123')
        self.wallet = Wallet.objects.create(user=self.user, balance=100.00)
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_wallet(self):
        response = self.client.get(f'/api/v1/wallets/{self.wallet.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], '100.00')

    def test_create_wallet(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post('/api/v1/wallets/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_wallet(self):
        data = {'balance': '150.00'}
        response = self.client.patch(f'/api/v1/wallets/{self.wallet.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], '150.00')

    def test_delete_wallet(self):
        response = self.client.delete(f'/api/v1/wallets/{self.wallet.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Wallet.objects.filter(id=self.wallet.id).exists())


class TransactionViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123')
        refresh = RefreshToken.for_user(self.user1)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_transaction(self):
        # Cria carteiras fictícias no banco de dados
        wallet1 = Wallet.objects.create(user=self.user1, balance=200.00)
        wallet2 = Wallet.objects.create(user=self.user2, balance=50.00)

        data = {'receiver_wallet': wallet2.id, 'amount': '50.00'}
        response = self.client.post('/api/v1/transactions/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.sender_wallet, wallet1)
        self.assertEqual(transaction.receiver_wallet, wallet2)
        self.assertEqual(transaction.amount, Decimal('50.00'))
        self.assertEqual(transaction.status, 'completed')
        wallet1.refresh_from_db()
        wallet2.refresh_from_db()
        self.assertEqual(wallet1.balance, Decimal('100.00'))
        self.assertEqual(wallet2.balance, Decimal('100.00'))

    def test_insufficient_funds(self):
        # Cria carteiras fictícias no banco de dados
        wallet1 = Wallet.objects.create(user=self.user1, balance=200.00)
        wallet2 = Wallet.objects.create(user=self.user2, balance=100.00)

        data = {'sender_wallet': wallet1.id, 'receiver_wallet': wallet2.id, 'amount': '300.00'}
        response = self.client.post('/api/v1/transactions/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Saldo insuficiente.')
