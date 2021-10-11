from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsModer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_moder
        else:
            return False


class IsMuted(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return not request.user.is_muted
        else:
            return False


class IsBaned(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return not request.user.is_banned
        else:
            return False