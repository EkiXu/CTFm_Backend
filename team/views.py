from venv import create
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework import status, viewsets,mixins

from team import models
from team import serializers
from team import permissions

# Create your views here.

class TeamViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.Team.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.DetailedTeamSerializer
        elif self.action == "update":
            return serializers.DetailedTeamSerializer
        elif self.action == "create":
            return serializers.CreateTeamSerializer
        elif self.action == "joinTeam":
            return serializers.JoinTeamSerializer
        else : 
            return serializers.BaseTeamSerializer
    
    def create(self, request, *args, **kwargs):
        request.data["leader"] = request.user.pk
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'retrieve' or self.action == "list" or self.action == "joinTeam":
            permission_classes = [permissions.IsVerified]
        elif self.action == "update" or self.action == 'destory':
            permission_classes = [permissions.IsLeaderOrAdmin]
        else:
            permission_classes = [permissions.IsLeaderOrAdmin]
        return [permission() for permission in permission_classes]

    @action(detail=False,methods=['POST'],url_name='joinTeam',url_path='ticket')
    def joinTeam(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = serializer.data["token"]
            user = request.user
            if user.team:
                return Response({"detail":f"Already Joined A Team"},status=status.HTTP_400_BAD_REQUEST)
            team:models.Team
            try:
                team = models.Team.objects.get(token=token)
                user.team = team
                user.save()
                return Response(serializers.DetailedTeamSerializer(data=team),status=status.HTTP_200_OK)
            except models.Team.DoesNotExist as e:
                return Response({"detail":f"Token Error"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":f"Token Error"},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        user = request.user
        team = self.get_object()
        if team.leader == user: 
            return super().destroy(request, *args, **kwargs)
        else:
            user.team = None
            user.save()
            return Response({"detail":f"Leaved Successfully"},status=status.HTTP_200_OK)
class AdminTeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.Team.objects.all()
    permission_classes = [permissions.IsAdmin]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.DetailedTeamSerializer
        elif self.action == "update":
            return serializers.DetailedTeamSerializer
        elif self.action == "create":
            return serializers.CreateTeamSerializer
        else : 
            return serializers.BaseTeamSerializer
