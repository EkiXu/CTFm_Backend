from user.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import prefetch_related_objects
from rest_framework import permissions, viewsets ,status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from challenge.models import Challenge,SolutionDetail,ChallengeCategory
from challenge import  serializers
class ChallengeCategoryViewSet(viewsets.ModelViewSet):
    """
    Project viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = ChallengeCategory.objects.all()
    serializer_class = serializers.ChallengeCategorySerializer
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        elif self.action == 'create':
            permission_classes = [permissions.IsAdminUser] 
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save()

class ChallengeViewSet(viewsets.ModelViewSet):
    """
    Challenge viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Challenge.objects.all()
    serializer_class = serializers.ChallengeSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        categoryName = self.request.query_params.get('categoryName', None)
        if categoryName is not None:
            try:
                category = ChallengeCategory.objects.get(name = categoryName)
            except ObjectDoesNotExist:
                return Challenge.objects.none()
            queryset = Challenge.objects.all()
            queryset = queryset.filter(category=category.id)
            return queryset
        else:
            return Challenge.objects.all()
    
    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ChallengeSerializer
        elif self.action == 'create':
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
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        elif self.action == 'create':
            permission_classes = [permissions.IsAdminUser] 
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True,methods=['POST'],url_name='checkFlag',url_path='_checkFlag')
    def checkFlag(self,request,pk=None,*args,**kwargs):
        challenge = self.get_object()
        flag = ""
        try:
            flag = request.data['flag']
            detail = SolutionDetail.objects.get(challenge = challenge, user = request.user)
            print(detail)
        except KeyError:
            return Response({'detail': 'Flag Field is NULL.'},status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            if challenge.flag == flag:
                user = request.user
                detail = SolutionDetail(challenge = challenge,user = user)
                detail.save()
                user.last_point_at = timezone.now()
                user.save(update_fields=["last_point_at"])
                return Response({'detail': 'Solved Successfully'})
            else:
                return Response({'detail': 'Wrong Flag'},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'detail': 'Already Solved'},status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=True,methods=['GET'],url_name='Solved',url_path='_solved')
    def solved(self,request,pk=None,*args,**kwargs):
        challenge = self.get_object()
        try:
            detail = SolutionDetail.objects.get(challenge = challenge, user = request.user)
        except ObjectDoesNotExist:
             return Response({'solved': False},status=status.HTTP_200_OK)
        return Response({'solved': True},status=status.HTTP_200_OK)
    
    def perform_create(self, serializer):
        serializer.save()

class CategoryChallengeViewset(ChallengeViewSet):
    def get_queryset(self):
        return Challenge.objects.filter(category=self.kwargs['category_pk']).order_by('id')