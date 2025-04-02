from django.contrib import admin
from .models import Wallet, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('get_user_email', 'balance', 'created_at', 'updated_at')
    search_fields = ('user__email',)
    list_select_related = ('user',)

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Usuário'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.refresh_from_db()


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'get_sender_email',
        'get_receiver_email',
        'amount',
        'status',
        'timestamp'
    )
    list_filter = ('status', 'timestamp')
    search_fields = (
        'sender_wallet__user__email',
        'receiver_wallet__user__email',
    )

    def get_sender_email(self, obj):
        return obj.sender_wallet.user.email
    get_sender_email.short_description = 'Remetente'

    def get_receiver_email(self, obj):
        return obj.receiver_wallet.user.email
    get_receiver_email.short_description = 'Destinatário'
