from rest_framework import permissions


class IsCurrentUserOrReadOnly(permissions.BasePermission):
    """
        Permission that checks is user has access as owner or not.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        print(f'----------Are you current user {obj==request.user}')
        return obj == request.user


class IsSellerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'seller'):
            return True
        return False


class IsSellerOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.seller == obj.seller:
            return True
        return False

