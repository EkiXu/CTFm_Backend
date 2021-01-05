from django.shortcuts import render
from contest import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from contest.models import Contest
from contest import serializers

class ContestManager(APIView):
    """
    Get Contest Detail And Update Contest Detail
    """
    permission_classes = [permissions.IsAdminOrReadOnly]
    
    def get(self, request, format=None):
        contest = Contest.objects.all().first()
        serializer = serializers.ContestSerializer(contest)
        return Response(serializer.data)

    def put(self, request, format=None):
        contest = Contest.objects.all().first()
        serializer = serializers.ContestSerializer(contest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
