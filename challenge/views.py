from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from rest_framework import viewsets ,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_extensions.cache.decorators import (cache_response)
from rest_framework_extensions.mixins import NestedViewSetMixin


from challenge.models import Challenge,SolutionDetail,ChallengeCategory
from challenge import serializers
from challenge import throttles
from challenge import utils
from challenge import permissions

from contest.utils import contest_began_or_forbbiden,in_contest_time_or_forbbiden

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

class ChallengeCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Project viewset automatically provides `list`, `retrieve`
    """
    queryset = ChallengeCategory.objects.all()
    serializer_class = serializers.ChallengeCategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsVerified]

    @contest_began_or_forbbiden
    @cache_response(key_func=utils.ChallengeCategoryListKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @contest_began_or_forbbiden
    @cache_response(key_func=utils.ChallengeCategoryObjectKeyConstructor())
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
class AdminChallengeCategoryViewSet(viewsets.ModelViewSet):
    """
    Project viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = ChallengeCategory.objects.all()
    serializer_class = serializers.FullChallengeCategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminUser]


class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Challenge viewset automatically provides `list`, retrieve`
    """
    queryset = Challenge.objects.all().filter(is_hidden=False)
    serializer_class = serializers.ChallengeSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `categoryName` query parameter in the URL.
        """
        queryset = Challenge.objects.all()
        categoryName = self.request.query_params.get('categoryName', None)
        if categoryName is not None:
            try:
                category = ChallengeCategory.objects.get(name__iexact = categoryName)
            except ObjectDoesNotExist:
                return Challenge.objects.none()
            queryset = queryset.filter(category=category.id)
        
        if self.action == "getFull" or self.action == "getFullDetail" or self.action == "update":
            return queryset
        return queryset.filter(is_hidden=False)
    
    def get_throttles(self):
        if self.action == "checkFlag":
            throttle_classes = [throttles.TenPerMinuteUserThrottle]
        else: 
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ChallengeSerializer
        elif self.action == 'create' or self.action ==  'update':
            return serializers.FullChallengeSerializer
        elif self.action == "checkFlag":
            return serializers.FlagSerializer
        else : 
            return serializers.ChallengeDetailSerializer
    
    @contest_began_or_forbbiden
    @cache_response(key_func=utils.ChallengeListKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @contest_began_or_forbbiden
    @cache_response(key_func=utils.ChallengeObjectKeyConstructor())
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.IsVerified]
        return [permission() for permission in permission_classes]


    @action(detail=True,methods=['POST'],url_name='checkFlag',url_path='_checkFlag')
    @in_contest_time_or_forbbiden
    def checkFlag(self,request,pk=None,*args,**kwargs):
        challenge = self.get_object()
        flag = "" 
        try:
            flag = request.data['flag']
            detail = SolutionDetail.objects.get(challenge = challenge, user = request.user)
        except KeyError:
            return Response({'detail': 'Flag Field is NULL.'},status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            user = request.user
            detail = SolutionDetail(challenge = challenge,user = user,solved = False)
                
        if detail.solved == True:
            return Response({'detail': 'Already Solved'},status=status.HTTP_400_BAD_REQUEST)
        else:
            detail.times += 1
            
            if challenge.flag == flag:
                user = request.user
                detail.solved = True
                detail.save()
                user.last_point_at = timezone.now()
                user.save(update_fields=["last_point_at"])
                cache.set("rank_updated_at", datetime.utcnow())
                cache.set("challenge_points_updated_at", datetime.utcnow())
                amount = challenge.solved_amount
                if amount < 3: 
                    msg = f"Congratulations to [{request.user}] for getting the {utils.challenge_bloods[amount-1]} of [{challenge.title}]"
                    async_to_sync(channel_layer.group_send)("challenge", {"type": "challenge.message", "message": msg}) 
                return Response({'detail': 'Solved Successfully'})
            else:
                detail.save()
                return Response({'detail': 'Wrong Flag'},status=status.HTTP_400_BAD_REQUEST)

class AdminChallengeViewSet(viewsets.ModelViewSet):
    """
    Challenge viewset automatically provides `list`, `create`,
    `retrieve`,`update` and `destroy` actions.
    """
    queryset = Challenge.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ChallengeSerializer
        else : 
            return serializers.FullChallengeSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `categoryName` query parameter in the URL.
        """
        queryset = Challenge.objects.all()
        categoryName = self.request.query_params.get('categoryName', None)
        if categoryName is not None:
            try:
                category = ChallengeCategory.objects.get(name = categoryName)
            except ObjectDoesNotExist:
                return Challenge.objects.none()
            queryset = queryset.filter(category=category.id)
        return queryset

class CategoryChallengeViewset(NestedViewSetMixin,ChallengeViewSet):
    pass