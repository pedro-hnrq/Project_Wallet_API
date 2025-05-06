from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import User
from django.utils.translation import gettext_lazy as _


class Wallet(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='wallet',
        verbose_name='Usuário',
        db_index=True
    )
    balance = models.DecimalField(
        _('Saldo'),
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00)]
    )
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)

    class Meta:
        db_table = 'wallets'
        ordering = ('-created_at',)
        verbose_name = _('Carteira')
        verbose_name_plural = _('Carteiras')

    def __str__(self):
        return f"Carteira de {self.user.email}"


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('completed', 'Concluída'),
        ('failed', 'Falhou'),
    ]

    sender_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='sent_transactions',
        verbose_name='Carteira do Remetente'
    )
    receiver_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='received_transactions',
        verbose_name='Carteira do Destinatário'
    )
    amount = models.DecimalField(
        _('Valor'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    timestamp = models.DateTimeField('Data/Hora', auto_now_add=True)
    note = models.TextField('Observação', blank=True, null=True)

    class Meta:
        db_table = 'transactions'
        ordering = ('-timestamp',)
        verbose_name = _('Transação')
        verbose_name_plural = _('Transações')
        constraints = [
            models.CheckConstraint(
                check=~models.Q(sender_wallet=models.F('receiver_wallet')),
                name='sender_different_from_receiver'
            ),
            models.CheckConstraint(
                check=models.Q(amount__gt=0),
                name='amount_greater_than_zero'
            )
        ]

    def __str__(self):
        return f"Transação de R${self.amount} entre {self.sender_wallet.user.email} e {self.receiver_wallet.user.email}"
