from rest_framework import serializers
from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Wallet
        fields = ('id', 'user_email', 'balance', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user_email', 'created_at', 'updated_at')


class TransactionSerializer(serializers.ModelSerializer):
    sender_email = serializers.ReadOnlyField(source='sender_wallet.user.email')
    receiver_email = serializers.ReadOnlyField(source='receiver_wallet.user.email')
    receiver_wallet = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all())
    sender_wallet = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'sender_wallet', 'sender_email', 'receiver_email', 'receiver_wallet', 'amount', 'status', 'timestamp', 'note')
        read_only_fields = ('id', 'sender_wallet', 'sender_email', 'receiver_email', 'timestamp', 'status')
