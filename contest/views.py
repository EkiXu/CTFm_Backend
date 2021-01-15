from heapq import nlargest
from django.contrib.auth import get_user_model
from django.db.models import query
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from contest import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework_extensions.cache.decorators import (
    cache_response
)

from challenge.models import SolutionDetail
from user.serializers import UserSerializer

from contest.models import Contest
from contest import serializers
from contest import utils

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

class TopTenTrendView(APIView):
    @cache_response(key_func=utils.TopTenTrendKeyConstructor())
    def get(self, request, format=None):
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

class ScoreBoardView(ListAPIView):
    queryset = sorted(UserModel.objects.all().filter(is_hidden=False), key=lambda t: t.points,reverse=True)
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    @cache_response(key_func=utils.ScoreboardKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    