from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WalletDetailView, TransactionViewSet


router = DefaultRouter()
router.register('wallets', WalletDetailView)
router.register('transactions', TransactionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
