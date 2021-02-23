from heapq import nlargest

from django.contrib.auth import get_user_model
from django.db.models import Q, query
from django.conf import settings

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework_extensions.cache.decorators import cache_response

from challenge.models import Challenge, SolutionDetail
from challenge.serializers import TinyChallengeSerializer

from contest import paginations
from contest import models
from contest import serializers
from contest import utils

UserModel = get_user_model()

class ContestManager(APIView):
    """
    Get Contest Detail And Update Contest Detail
    """
    @cache_response(60*60*24,key_func=utils.ContestKeyConstructor())
    def get(self, request, format=None):
        contest = models.Contest.objects.get(pk=1)
        serializer = serializers.ContestSerializer(contest)
        return Response(serializer.data)


class AdminContestManager(APIView):
    """
    Get Contest Detail And Update Contest Detail
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request, format=None):
        contest = models.Contest.objects.all().first()
        serializer = serializers.ContestSerializer(contest)
        return Response(serializer.data)

    def put(self, request, format=None):
        contest = models.Contest.objects.all().first()
        serializer = serializers.ContestSerializer(contest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TopTenTrendView(APIView):
    queryset = UserModel.objects.all()
    def get_queryset(self):
        query = self.queryset.all()
        return query

    @cache_response(key_func=utils.TopTenTrendKeyConstructor())
    def get(self, request, format=None):
        users = nlargest(10,self.get_queryset(),key=lambda t: t.points)
        rows = []
        for user in users:
            history = SolutionDetail.objects.filter(user = user).filter(solved=True).filter(challenge__is_hidden=False).order_by('pub_date')
            cur_points = 0
            data = []
            for record in history:
                cur_points += record.challenge.points
                data.append({"points":cur_points,"date":record.pub_date})
            rows.append({"id":user.id,"nickname":user.nickname,"current_points":cur_points,"records":data})
        return Response({"rows":rows},status=status.HTTP_200_OK)

class ScoreboardView(ListAPIView):
    serializer_class = serializers.ScoreboardSerializer
    pagination_class = paginations.ScoreboardPagination
    queryset = UserModel.objects.all().filter(is_hidden=False)

    @cache_response(key_func=utils.ScoreboardKeyConstructor())
    def list(self, request, *args, **kwargs):
        playerQueryset = sorted(self.get_queryset(), key=lambda t: t.points,reverse=True)
        challengeQueryset = Challenge.objects.all().filter(is_hidden=False)
        challengeSerializer = TinyChallengeSerializer(challengeQueryset, many=True)
        
        page = self.paginate_queryset(playerQueryset)
        if page is not None:
            serializer = serializers.ScoreboardSerializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data,challengeSerializer.data)

        playerSerializer = serializers.ScoreboardSerializer(playerQueryset, many=True)
        return Response({"challenges":challengeSerializer.data,"players":playerSerializer.data})
    
class StuTopTenTrendView(TopTenTrendView):
    queryset = UserModel.objects.filter(Q(email__endswith=settings.SCHOOL_EMAIL_SUFFIX))

class StuScoreboardView(ScoreboardView):
    queryset = UserModel.objects.filter(Q(email__endswith=settings.SCHOOL_EMAIL_SUFFIX))