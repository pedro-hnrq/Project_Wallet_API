from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WalletsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wallets'
    verbose_name = _('Carteira Digital')
    verbose_name_plural = _('Carteiras Digital')

    def ready(self):
        import wallets.signals
