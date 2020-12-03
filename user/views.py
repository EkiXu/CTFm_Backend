#from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from user import serializers
from user.pemissions import IsOwner, IsOwnerOrAdmin

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    """
    Logout by sending token
    """
    try:
        token = RefreshToken(request.data['token'])
        token.blacklist()
        return Response({"detail":"block successfully"},status=status.HTTP_200_OK)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """
    Register
    """
    serializer = serializers.RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def obtainToken(request):
    """
    Login
    """
    try:
        username = request.data['username']
        password = request.data['password']
    except KeyError:
        return Response({"detail":"username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
    user = auth.authenticate(username=username, password=password)
    if not user:
        return Response({"detail":"Wrong Username or Password"}, status=status.HTTP_400_BAD_REQUEST)
    refresh = serializers.MyTokenObtainPairSerializer.get_token(user)
    return Response({"refresh":str(refresh),"access": str(refresh.access_token)})

class UserViewSet(viewsets.ModelViewSet):
    """
    User viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = User.objects.all()

    pagination_class = LimitOffsetPagination
    def get_serializer_class(self):
        if self.action == "create":
            return serializers.RegisterSerializer
        elif self.action == "retrieve":
            return serializers.UserDetailSerializer
        elif self.action == 'update':
            return serializers.UserDetailUpdateSerializer
        else : 
            return serializers.UserSerializer
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        elif self.action == 'retrieve' or self.action == 'update':
            permission_classes = [permissions.IsAuthenticated,IsOwnerOrAdmin]
        elif self.action == 'create':
            permission_classes = [permissions.IsAdminUser] 
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save()



    def update(self, request, *args, **kwargs):
        try:
            username = request.user.username
            password = request.data['old_password']
        except KeyError:
            return Response({"detail":"Password are required."}, status=status.HTTP_400_BAD_REQUEST)
        if request.user and request.user.is_staff:
            user = self.get_object()
        else: 
            user = auth.authenticate(username=username, password=password)
        if not user:
            return Response({"detail":"Wrong Password"}, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = request.data.get('new_password',None)

        if new_password:
            if len(new_password) >= 8:
                user.set_password(new_password)
                user.save()
            else: 
                return Response({"detail":"New Password too short"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.UserDetailUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


        