from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_extensions.cache.decorators import (cache_response)
from rest_framework_extensions.mixins import NestedViewSetMixin

from challenge.models import Challenge, SolutionDetail, ChallengeCategory
from challenge import serializers
from challenge import throttles
from challenge.throttles import ThirtyPerMinuteUserThrottle as ChallengThrottleRate
from challenge import utils
from challenge import permissions
from challenge import models
from dynamic.control_utils import ControlUtils
from dynamic.models import ChallengeContainer
from dynamic.redis_utils import RedisUtils
from dynamic.db_utils import DBUtils
from dynamic.serializers import BaseChallengeContainerSerializer

from contest.utils import contest_began_or_forbbiden, in_contest_time_or_forbbiden

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
    permission_classes = [permissions.IsVerifiedAndInTeam]

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
        queryset = Challenge.objects.all().filter(is_hidden=False)
        categoryName = self.request.query_params.get('categoryName', None)
        if categoryName is not None:
            try:
                category = ChallengeCategory.objects.get(name__iexact=categoryName)
            except ObjectDoesNotExist:
                return Challenge.objects.none()
            queryset = queryset.filter(category=category.id)

        # if self.action == "getFull" or self.action == "getFullDetail" or self.action == "update":
        #     return queryset
        return queryset.filter(is_hidden=False)

    def get_throttles(self):
        if self.action == "check_action" or self.action:
            throttle_classes = [ChallengThrottleRate]
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ChallengeSerializer
        elif self.action == 'create' or self.action == 'update':
            return serializers.FullChallengeSerializer
        elif self.action == "check_flag":
            return serializers.FlagSerializer
        else:
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
        permission_classes = [permissions.IsVerifiedAndInTeam]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['POST'], url_name='checkFlag', url_path='_checkFlag')
    @in_contest_time_or_forbbiden
    def check_flag(self, request, pk=None, *args, **kwargs):
        challenge = self.get_object()
        flag = ""
        team = request.user.team
        if team == None:
            return Response({'detail': 'Create or Join A Team to Play The Game.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            flag = request.data['flag']
            #detail = SolutionDetail.objects.get(challenge=challenge, user=request.user)
            detail = SolutionDetail.objects.filter(challenge=challenge, team=team, solved=True)[0]
        except KeyError:
            return Response({'detail': 'Flag Field is NULL.'}, status=status.HTTP_400_BAD_REQUEST)
        except (ObjectDoesNotExist, IndexError):
            user = request.user
            detail = SolutionDetail(challenge=challenge, user=user, team=user.team, solved=False)
        
        if detail.solved:
            return Response({'detail': 'Already Solved'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            detail.times += 1

            # Implementation for dynamic flags. LemonPrefect<me@lemonprefect.cn>
            if challenge.has_dynamic_container:
                user = request.user
                container = ControlUtils.get_user_challenge_container(user, challenge)
                if container is None:
                    return Response(
                        {'detail': 'Container should have been launched at first.'},
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                challenge_flag = container.flag
            else:
                challenge_flag = challenge.flag # Prevent the vairiable pollution of challenge.flag for not making the static flag ambigious.

            if challenge_flag == flag:
                user = request.user
                detail.solved = True
                detail.save()
                user.last_point_at = timezone.now()
                user.save(update_fields=["last_point_at"])

                cache.set("rank_updated_at", datetime.utcnow())
                cache.set("challenge_points_updated_at", datetime.utcnow())
                amount = challenge.solved_amount
                if amount <= 3:
                    detail = f"Congratulations to [{request.user}] from [{user.team.name}] for getting the {utils.challenge_bloods[amount - 1]} of [{challenge.title}]"
                    async_to_sync(channel_layer.group_send)("challenge", {"type": "challenge.message", "message": detail})
                return Response({'detail': 'Solved Successfully'})
            else:
                detail.save()
                return Response({'detail': 'Wrong Flag'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_container(self,request,challenge:models.Challenge,pk=None,*args,**kwargs):
        user = request.user
        try:
            container = ControlUtils.get_user_challenge_container(user, challenge)
            if container == None:
                return Response(data={"detail": "No Container"}, status=status.HTTP_204_NO_CONTENT)
            serializer = BaseChallengeContainerSerializer(instance=container)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

    def add_container(self,request,challenge:models.Challenge,pk=None,*args,**kwargs):
        user = request.user
        redis_util = RedisUtils(user.id)

        if not redis_util.acquire_lock():
            return Response(data={'detail': 'Request Too Fast!'},status=status.HTTP_400_BAD_REQUEST)

        configs = DBUtils.get_all_configs()

        if int(configs.get("user_max_container_count","2")) <= user.container_count:
            return Response(data={'detail': 'Your max container count exceed.'},status=status.HTTP_400_BAD_REQUEST)
        
        current_count = DBUtils.get_all_alive_container_count()
        if int(configs.get("docker_max_container_count","2000")) <= int(current_count):
            return Response(data={'detail': 'Server max container count exceed.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        flag = ControlUtils.gen_random_flag()
        container:ChallengeContainer
        if challenge.protocol == Challenge.HTTP:
            container = ControlUtils.add_user_container(user.id, challenge.id, flag=flag)
        else:
            port = redis_util.get_available_port()
            container = ControlUtils.add_user_container(user.id, challenge.id, flag=flag, port=port)

        redis_util.release_lock()

        serializer = BaseChallengeContainerSerializer(instance=container)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def renew_container(self,request,challenge:models.Challenge,pk=None,*args,**kwargs):
        user = request.user
        redis_util = RedisUtils(user.id)
        if not redis_util.acquire_lock():
            return Response(data={'success': False, 'detail': 'Request Too Fast!'},status=status.HTTP_400_BAD_REQUEST)

        configs = DBUtils.get_all_configs()
        
        docker_max_renew_count = int(configs.get("docker_max_renew_count"))
        container = ControlUtils.get_user_challenge_container(user,challenge)
        if container is None:
            return Response(data={'success': False, 'detail': 'Instance not found.'},status=status.HTTP_204_NO_CONTENT)
        if container.renew_count >= docker_max_renew_count:
            return Response(data={'success': False, 'detail': 'Max renewal times exceed.'})
        
        container = ControlUtils.renew_user_challenge_container(user.id, challenge.id)
        redis_util.release_lock()
        serializer = BaseChallengeContainerSerializer(instance=container)
        return  Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_container(self,request,challenge:models.Challenge,pk=None,*args,**kwargs):
        user = request.user
        redis_util = RedisUtils(user.id)
        if not redis_util.acquire_lock():
            return Response(data={'success': False, 'detail': 'Request Too Fast!'})

        if ControlUtils.remove_user_challenge_container(user.id,challenge.id):
            redis_util.release_lock()

            return Response(data={'success': True})
        else:
            return Response(data={'success': False, 'detail': 'Failed when destroy instance, please contact admin!'})

    @action(detail=True, methods=['GET', 'POST','PATCH', 'DELETE'], url_name='manage_environment', url_path='env',throttle_classes=[throttles.ContainerRateThrottle])
    @contest_began_or_forbbiden
    def manage_container(self, request, pk=None, *args, **kwargs):
        """
        Retrive, Create, Renew  and Delete Dynamic Container
        """
        challenge: models.Challenge = self.get_object()
        if not challenge.has_dynamic_container:
            return Response(data={"detail": "Challenge do not support Dynamic Container"},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'GET':
            # try:
            #     container = ControlUtils.get_user_challenge_container(user, challenge)
            #     serializer = containerSerializer(instance=container)
            #     return Response(serializer.data, status=status.HTTP_200_OK)
            # except ObjectDoesNotExist as de:
            #     return Response(data={"detail": str(de)}, status=status.HTTP_204_NO_CONTENT)
            # except Exception as e:
            #     return Response(data={"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return self.get_container(request,challenge,pk,*args, **kwargs)
        elif request.method == 'POST':
            # try:
            #     container = ControlUtils.add_user_container(user, challenge)
            #     serializer = containerSerializer(instance=container)
            #     return Response(serializer.data, status=status.HTTP_201_CREATED)
            # except Exception as e:
            #     raise e
            #     return Response(data={"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return self.add_container(request,challenge,pk,*args, **kwargs)
        elif request.method == 'PATCH':
            return self.renew_container(request,challenge,pk,*args, **kwargs)
            # try:
            #     container = ControlUtils.renew_user_container(user, challenge)
            #     serializer = containerSerializer(instance=container)
            #     return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            # except Exception as e:
            #     return Response(data={"detail":  str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif request.method == 'DELETE':
            return self.delete_container(request,challenge,pk,*args, **kwargs)
            # try:
            #     ControlUtils.remove_user_container(user, challenge)
            #     return Response(data={"detail":"delete successfully"}, status=status.HTTP_202_ACCEPTED)
            # except Exception as e:
            #     return Response(data={"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        else:
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
                category = ChallengeCategory.objects.get(name=categoryName)
            except ObjectDoesNotExist:
                return Challenge.objects.none()
            queryset = queryset.filter(category=category.id)
        return queryset


class CategoryChallengeViewset(NestedViewSetMixin, ChallengeViewSet):
    pass
