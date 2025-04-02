from rest_framework import permissions


class IsTransactionOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.sender_wallet.user == request.user or obj.receiver_wallet.user == request.user
