from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction
from django.db import transaction


@receiver(post_save, sender=Transaction)
def update_wallet_balance(sender, instance, created, **kwargs):
    if not created and instance.status == 'completed':
        with transaction.atomic():
            sender_wallet = instance.sender_wallet
            receiver_wallet = instance.receiver_wallet
            amount = instance.amount

            if sender_wallet.balance >= amount:
                sender_wallet.balance -= amount
                receiver_wallet.balance += amount
                print(f"Transação {instance.id} concluída com sucesso.")
                print(f"Saldo atual do remetente: {sender_wallet.balance}")
                print(f"Saldo atual do destinatário: {receiver_wallet.balance}")
                sender_wallet.save()
                receiver_wallet.save()
            else:
                # Saldo insuficiente, atualiza o status para "falhou"
                instance.status = 'failed'
                instance.save()
                print(f"Transação {instance.id} falhou devido a saldo insuficiente.")
