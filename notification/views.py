from notification.models import Notification
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from notification import serializers
# Create your views here.

class NotificationViewSet(viewsets.ModelViewSet):
    """
    Notification viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    pagination_class = LimitOffsetPagination
    
    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return serializers.NotificationSerializer
        else : 
            return serializers.NotificationSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create" or self.action == "update" or self.action == "delete":
            permission_classes = [permissions.IsAdminUser] 
        else : 
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
            
        return [permission() for permission in permission_classes]
