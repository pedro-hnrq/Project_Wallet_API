from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from .permissions import IsTransactionOwner
from drf_spectacular.utils import extend_schema
from django.db import transaction
from decimal import Decimal


@extend_schema(tags=['Wallets'])
class WalletDetailView(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            wallet = queryset.first()
            serializer = self.get_serializer(wallet)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Carteira não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        """Cria uma carteira para o usuário autenticado, se não existir."""
        if Wallet.objects.filter(user=request.user).exists():
            return Response({'detail': 'Carteira já existe para este usuário.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Atualiza a carteira do usuário autenticado."""
        try:
            instance = Wallet.objects.get(pk=kwargs['pk'])
        except Wallet.DoesNotExist:
            return Response({'detail': 'Carteira não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        if instance.user != request.user:
            return Response({'detail': 'Você não tem permissão para atualizar esta carteira.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.pop('partial', False))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Deleta a carteira do usuário autenticado."""
        try:
            instance = Wallet.objects.get(pk=kwargs['pk'])
        except Wallet.DoesNotExist:
            return Response({'detail': 'Carteira não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        if instance.user != request.user:
            return Response({'detail': 'Você não tem permissão para deletar esta carteira.'}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Transactions'])
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsTransactionOwner]

    def get_queryset(self):
        """Retorna as transações do usuário autenticado como remetente ou destinatário."""
        return Transaction.objects.filter(sender_wallet__user=self.request.user) | Transaction.objects.filter(receiver_wallet__user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Obter carteira do remetente
        try:
            sender_wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            return Response(
                {'detail': 'Carteira do remetente não encontrada.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar destinatário
        receiver_wallet_id = request.data.get('receiver_wallet')
        try:
            receiver_wallet = Wallet.objects.get(pk=receiver_wallet_id)
        except Wallet.DoesNotExist:
            return Response(
                {'detail': 'Carteira do destinatário não encontrada.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar transferência para si mesmo
        if sender_wallet == receiver_wallet:
            return Response(
                {'detail': 'Não é possível transferir para a mesma carteira.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar valor
        try:
            amount = Decimal(request.data.get('amount'))
        except ValueError:
            return Response(
                {'detail': 'Valor inválido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if amount <= Decimal('0.00'):
            return Response(
                {'detail': 'O valor deve ser maior que zero.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar saldo suficiente
        if sender_wallet.balance < amount:
            return Response(
                {'detail': 'Saldo insuficiente.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Realizar operação atômica
        with transaction.atomic():
            # Criar transação
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            transaction_obj = serializer.save(
                sender_wallet=sender_wallet,
                status='completed'
            )
            transaction_obj.save()
            # Atualizar saldos
            sender_wallet.balance -= amount
            sender_wallet.save()

            receiver_wallet.balance += amount
            receiver_wallet.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Atualiza uma transação específica do usuário autenticado."""
        try:
            instance = Transaction.objects.get(pk=kwargs['pk'])
        except Transaction.DoesNotExist:
            return Response({'detail': 'Transação não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        if instance.sender_wallet.user != request.user and instance.receiver_wallet.user != request.user:
            return Response({'detail': 'Você não tem permissão para atualizar esta transação.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Deleta uma transação específica do usuário autenticado."""
        try:
            instance = Transaction.objects.get(pk=kwargs['pk'])
        except Transaction.DoesNotExist:
            return Response({'detail': 'Transação não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        if instance.sender_wallet.user != request.user and instance.receiver_wallet.user != request.user:
            return Response({'detail': 'Você não tem permissão para deletar esta transação.'}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
