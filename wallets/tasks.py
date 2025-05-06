from celery import shared_task
from django.utils import timezone
from .models import Transaction


@shared_task
def notify_transaction_created(tx_id):
    """
    Após 5s, imprime no terminal que a transação foi criada.
    """
    tx = Transaction.objects.select_related('sender_wallet__user', 'receiver_wallet__user').get(pk=tx_id)
    print(f"[{timezone.now()}] Transaction CREATED: "
          f"{tx.status.upper()} | "
          f"From: {tx.sender_wallet.user.email} -> To: {tx.receiver_wallet.user.email} | "
          f"Amount: {tx.amount}")


@shared_task
def notify_transaction_updated(tx_id):
    """
    Após 5s, imprime no terminal que a transação foi atualizada.
    """
    tx = Transaction.objects.select_related('sender_wallet__user', 'receiver_wallet__user').get(pk=tx_id)
    print(f"[{timezone.now()}] Transaction UPDATED: "
          f"{tx.status.upper()} | "
          f"From: {tx.sender_wallet.user.email} -> To: {tx.receiver_wallet.user.email} | "
          f"Amount: {tx.amount}")


@shared_task
def notify_transaction_deleted(sender_email, receiver_email, status, amount):
    """
    Após 5s, imprime no terminal que a transação foi deletada.
    Recebe dados avulsos porque o objeto já não existe no DB.
    """
    print(f"[{timezone.now()}] Transaction DELETED: "
          f"{status.upper()} | "
          f"From: {sender_email} -> To: {receiver_email} | "
          f"Amount: {amount}")
