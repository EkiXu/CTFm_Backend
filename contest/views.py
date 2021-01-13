from django.contrib.auth import get_user_model
from django.db.models import query
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from contest import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser,IsAuthenticated

from contest.models import Contest
from contest import serializers

from challenge.models import SolutionDetail
from user.serializers import UserSerializer

UserModel = get_user_model()

class ContestManager(APIView):
    """
    Get Contest Detail And Update Contest Detail
    """

    def get(self, request, format=None):
        contest = Contest.objects.all().first()
        serializer = serializers.ContestSerializer(contest)
        return Response(serializer.data)


class AdminContestManager(APIView):
    """
    Get Contest Detail And Update Contest Detail
    """
    permission_classes = [IsAdminUser]
    
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTopTenTrend(request):
    from heapq import nlargest
    users = nlargest(10,UserModel.objects.all(),key=lambda t: t.points)
    rows = []
    for user in users:
        history = SolutionDetail.objects.filter(user = user).order_by('pub_date')
        cur_points = 0
        data = []
        for record in history:
            cur_points += record.challenge.points
            data.append({"points":cur_points,"date":record.pub_date})
        rows.append({"id":user.id,"nickname":user.nickname,"current_points":cur_points,"records":data})
    return Response({"rows":rows},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getScoreBoard(request):
    users = sorted(UserModel.objects.all().filter(is_hidden=False), key=lambda t: t.points,reverse=True)
    serializer = UserSerializer(users,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)