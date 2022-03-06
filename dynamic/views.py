from django.shortcuts import render

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from dynamic import serializers
from dynamic import models
from rest_framework import status


from rest_framework.permissions import IsAdminUser,BasePermission

# Create your views here.

class UpdateWhaleConfigView(GenericAPIView):
    serializer_class = serializers.WhaleConfigSerializer
    queryset = models.WhaleConfig.objects.all()
    permission_classes = [IsAdminUser]
    def post(self, request, *args, **kwargs):
        data:dict = request.data
        ret = {}
        for key,value in data.items():
            obj, created = models.WhaleConfig.objects.update_or_create(
                key = key,
                defaults={"key":key,"value":value}
            )
            ret[obj.key]=obj.value
        return Response(ret, status=status.HTTP_200_OK)
    def get(self, request, *args, **kwargs):
        configs = models.WhaleConfig.objects.all()
        ret = {}
        for each in configs:
            ret[each.key] = each.value
        return Response(ret, status=status.HTTP_200_OK) 

class AdminContainerViewSet(viewsets.ModelViewSet):
    queryset = models.ChallengeContainer.objects.all()
    serializer_class = serializers.FullChallengeContainerSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminUser]