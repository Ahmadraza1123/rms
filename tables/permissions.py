from rest_framework.permissions import BasePermission

class IsAdminOrManager(BasePermission):

    def has_permission(self, request, view):

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return request.user.is_authenticated and request.user.role in ['admin', 'manager']


class IsCustomer(BasePermission):

    def has_permission(self, request, view):

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return request.user.is_authenticated and request.user.role == 'customer'
