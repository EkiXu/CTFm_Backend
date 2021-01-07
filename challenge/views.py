from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import prefetch_related_objects
from rest_framework import permissions, viewsets ,status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from challenge.models import Challenge,SolutionDetail,ChallengeCategory
from challenge import serializers

from contest.permissions import IsInContestTimeOrAdminOnly

class ChallengeCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Project viewset automatically provides `list`, `retrieve`
    """
    queryset = ChallengeCategory.objects.all()
    serializer_class = serializers.ChallengeCategorySerializer
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsInContestTimeOrAdminOnly]
        else:
            permission_classes = [permissions.IsAuthenticated,IsInContestTimeOrAdminOnly]

        return [permission() for permission in permission_classes]
    
class AdminChallengeCategoryViewSet(viewsets.ModelViewSet):
    """
    Project viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = ChallengeCategory.objects.all()
    serializer_class = serializers.FullChallengeCategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAdminUser]

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
                category = ChallengeCategory.objects.get(name = categoryName)
            except ObjectDoesNotExist:
                return Challenge.objects.none()
            queryset = queryset.filter(category=category.id)
        
        if self.action == "getFull" or self.action == "getFullDetail" or self.action == "update":
            return queryset
        return queryset.filter(is_hidden=False)
    
    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ChallengeSerializer
        elif self.action == 'create' or self.action ==  'update':
            return serializers.FullChallengeSerializer
        elif self.action == "checkFlag":
            return serializers.FlagSerializer
        else : 
            return serializers.ChallengeDetailSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsInContestTimeOrAdminOnly]
        else:
            permission_classes = [permissions.IsAuthenticated,IsInContestTimeOrAdminOnly]
        return [permission() for permission in permission_classes]

    @action(detail=True,methods=['POST'],url_name='checkFlag',url_path='_checkFlag')
    def checkFlag(self,request,pk=None,*args,**kwargs):
        challenge = self.get_object()
        flag = ""
        try:
            flag = request.data['flag']
            detail = SolutionDetail.objects.get(challenge = challenge, user = request.user)
        except KeyError:
            return Response({'detail': 'Flag Field is NULL.'},status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            if challenge.flag == flag:
                user = request.user
                detail = SolutionDetail(challenge = challenge,user = user,solved = True)
                detail.save()
                user.last_point_at = timezone.now()
                user.save(update_fields=["last_point_at"])
                return Response({'detail': 'Solved Successfully'})
            else:
                user = request.user
                detail = SolutionDetail(challenge = challenge,user = user)
                detail.save()
                return Response({'detail': 'Wrong Flag'},status=status.HTTP_400_BAD_REQUEST)
        detail.times += 1
        if detail.solved == True:
            return Response({'detail': 'Already Solved'},status=status.HTTP_400_BAD_REQUEST)
        else:
            if challenge.flag == flag:
                user = request.user
                detail.solved = True
                detail.save()
                user.last_point_at = timezone.now()
                user.save(update_fields=["last_point_at"])
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
    serializer_class = serializers.FullChallengeSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAdminUser]

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
    
    def get_serializer_class(self):
        if self.action == "list":
            return serializers.FullChallengeSerializer
        else : 
            return serializers.BaseChallengeSerializer

class CategoryChallengeViewset(ChallengeViewSet):
    def get_queryset(self):
        return Challenge.objects.filter(category=self.kwargs['category_pk']).filter(is_hidden=False).order_by('id')