from rest_framework import permissions

class IsCustomerOrReadOnly(permissions.BasePermission):


    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and getattr(request.user, "role", None) == "customer"

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.customer == request.user
