from rest_framework.permissions import BasePermission


class IsVerified(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active and request.user.is_verified)

class IsVerifiedAndInTeam(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active and request.user.is_verified and request.user.team != None)