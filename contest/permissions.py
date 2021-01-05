from rest_framework import permissions
from contest.models import Contest
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

class IsInContestTimeOrAdminOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        current_time = timezone.now()
        # Write permissions are only allowed to the owner of the snippet.
        '''
        try:
            contest = Contest.objects.first()
            return bool(contest.start_time < current_time and current_time < contest.end_time) or bool(request.user and request.user.is_staff)
        except ObjectDoesNotExist:
            return False
        '''
        return True
        
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_staff
        )