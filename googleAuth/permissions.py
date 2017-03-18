from rest_framework.compat import is_authenticated
from rest_framework.permissions import BasePermission


class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return not is_authenticated(request.user)

