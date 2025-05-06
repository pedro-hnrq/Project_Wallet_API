from django.contrib import admin
from django.utils.html import format_html
from .models import Wallet, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('get_user_email', 'balance', 'created_at', 'updated_at')
    search_fields = ('user__email',)
    list_select_related = ('user',)

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Usuário'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'get_sender_email',
        'get_receiver_email',
        'amount',
        'colored_status',
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

    def colored_status(self, obj):
        """
        Retorna o status com cor:
         - failed  → vermelho
         - pending → laranja
         - completed → verde
        """

        color_map = {
            'failed': 'red',
            'pending': 'orange',
            'completed': 'green',
        }
        color = color_map.get(obj.status, 'black')
        label = obj.get_status_display()  # usa o human-readable do choice
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            label
        )
    colored_status.short_description = 'Status'
    colored_status.admin_order_field = 'status'
