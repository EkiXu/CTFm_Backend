from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
import challenge
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
from user.models import User
from team.models import Team

from contest import paginations
from contest import models
from contest import serializers
from contest import utils

class ContestManager(APIView):
    """
    Get Contest Detail And Update Contest Detail
    """
    serializer_class = serializers.ContestSerializer

    @cache_response(60*60*24,key_func=utils.ContestKeyConstructor())
    def get(self, request, format=None):
        contest = models.Contest.objects.get(pk=1)
        serializer = self.serializer_class(contest)
        return Response(serializer.data)


class AdminContestManager(APIView):
    """
    Get Contest Detail And Update Contest Detail
    """
    permission_classes = [IsAdminUser]
    serializer_class = serializers.ContestSerializer
    
    def get(self, request, format=None):
        contest = models.Contest.objects.all().first()
        serializer = self.serializer_class(contest)
        return Response(serializer.data)

    def put(self, request, format=None):
        contest = models.Contest.objects.all().first()
        serializer = self.serializer_class(contest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TopTenTrendView(APIView):
    queryset = User.objects.all().filter(is_hidden = False)
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

class TopTenTeamTrendView(APIView):
    queryset = Team.objects.get_queryset()
    def get_queryset(self):
        query = self.queryset.all()
        return query

    @cache_response(key_func=utils.TopTenTrendKeyConstructor())
    def get(self, request, format=None):
        teams = nlargest(10,self.get_queryset(),key=lambda t: t.points)
        rows = []
        for team in teams:
            history = SolutionDetail.objects.filter(team = team).filter(solved=True).filter(challenge__is_hidden=False).order_by('pub_date')
            cur_points = 0
            data = []
            for record in history:
                cur_points += record.challenge.points
                data.append({"points":cur_points,"date":record.pub_date})
            rows.append({"id":team.id,"name":team.name,"current_points":cur_points,"records":data})
        return Response({"rows":rows},status=status.HTTP_200_OK)

class ScoreboardView(ListAPIView):
    serializer_class = serializers.ScoreboardSerializer
    pagination_class = paginations.ScoreboardPagination
    queryset = User.objects.all().filter(is_hidden=False)

    @cache_response(key_func=utils.ScoreboardKeyConstructor())
    def list(self, request, *args, **kwargs):
        playerQueryset = sorted(self.get_queryset(), key=lambda t: t.points,reverse=True)
        challengeQueryset = []
        if not utils.IsBeforeContest():
            challengeQueryset = Challenge.objects.all().filter(is_hidden=False)

        challengeSerializer = TinyChallengeSerializer(challengeQueryset, many=True)
        
        page = self.paginate_queryset(playerQueryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data,challengeSerializer.data)

        playerSerializer = self.get_serializer(playerQueryset, many=True)
        return Response({"challenges":challengeSerializer.data,"players":playerSerializer.data})

class TeamScoreboardView(ListAPIView):
    serializer_class = serializers.TeamScoreboardSerializer
    pagination_class = paginations.ScoreboardPagination
    queryset = Team.objects.all()

    @cache_response(key_func=utils.ScoreboardKeyConstructor())
    def list(self, request, *args, **kwargs):
        playerQueryset = sorted(self.get_queryset(), key=lambda t: t.points,reverse=True)
        challengeQueryset = []
        if not utils.IsBeforeContest():
            challengeQueryset = Challenge.objects.all()

        challengeSerializer = TinyChallengeSerializer(challengeQueryset, many=True)
        
        page = self.paginate_queryset(playerQueryset)
        if page is not None:
            serializer = serializers.TeamScoreboardSerializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data,challengeSerializer.data)

        playerSerializer = serializers.TeamScoreboardSerializer(playerQueryset, many=True)
        return Response({"challenges":challengeSerializer.data,"teams":playerSerializer.data})

class StuTopTenTrendView(TopTenTrendView):
    queryset = User.objects.filter(Q(email__endswith=settings.SCHOOL_EMAIL_SUFFIX))

class StuScoreboardView(ScoreboardView):
    queryset = User.objects.filter(Q(email__endswith=settings.SCHOOL_EMAIL_SUFFIX))