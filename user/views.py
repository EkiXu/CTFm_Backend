from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth
from django.contrib.auth.hashers import make_password,check_password
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes,action, throttle_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.mixins import RetrieveModelMixin,UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from user import serializers
from user import throttles
from user import pemissions
from user import utils

UserModel = auth.get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
@permission_classes([AllowAny])
@throttle_classes([throttles.TenPerMinuteUserThrottle])
def register(request):
    """
    Register
    """
    serializer = serializers.RegisterSerializer(data=request.data,context={"request": request})
    if serializer.is_valid():
        try:
            serializer.save()
        except:
            Response({"detail":"check your server config."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([throttles.TenPerMinuteUserThrottle])
def activate(request,user_id,token):
    """
    Activate
    """
    try:
        user = UserModel.objects.get(id=user_id)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and user.is_verified:
        return Response({"detail":"Already Verified."},status=status.HTTP_208_ALREADY_REPORTED)
    if user is not None and utils.account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        refresh = serializers.MyTokenObtainPairSerializer.get_token(user)
        return Response({"refresh":str(refresh),"access": str(refresh.access_token)})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([throttles.TenPerMinuteUserThrottle])
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


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([throttles.TenPerMinuteUserThrottle])
def resetPasswordRequest(request):
    """
    Send ResetPassword Email
    """
    serializer = serializers.EmailSerializer(data=request.data)
    email = ""
    if serializer.is_valid():
        email = serializer.data['email']
    else:
        return Response({"detail":"Invalid Email Address"},status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = UserModel.objects.get(email = email)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user == None:
        return Response({"detail":"Invalid Email Address"},status=status.HTTP_400_BAD_REQUEST)
    current_site = get_current_site(request)
    utils.sendResetPasswordmail(user,current_site=current_site)
    return Response({"detail":"Reset Password Email Sent.Please Check Your Mailbox."},status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([throttles.TenPerMinuteUserThrottle])
def resetPassword(request,user_id,token):
    """
    ResetPassword
    """
    try:
        user = UserModel.objects.get(id=user_id)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and not user.is_verified:
        return Response({"detail":"Invalid User"},status=status.HTTP_400_BAD_REQUEST)

    if user is not None and utils.account_activation_token.check_token(user, token):
        serializer = serializers.ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({"detail":"Password Reset Successful!"},status=status.HTTP_200_OK)
        else:
            return Response({"detail":"Invalid Password."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail":"Invalid Request"},status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(RetrieveModelMixin,
                    UpdateModelMixin,
                    GenericViewSet):
    """
    User viewset automatically provides `retrieve` and `update` actions.
    """
    queryset = UserModel.objects.all()
    pagination_class = LimitOffsetPagination
    
    def get_throttles(self):
        if self.action == "verifyEmail":
            throttle_classes = [throttles.TenPerMinuteUserThrottle]
        else: 
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.UserDetailSerializer
        elif self.action == 'update':
            return serializers.UserDetailUpdateSerializer
        elif self.action == 'sendVerifyEmail':
            return serializers.UserEmailSerializer
        else : 
            return serializers.UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'update':
            permission_classes = [pemissions.IsOwnerOrAdmin]
        elif self.action == 'getStatus' or self.action == 'sendVerifyEmail':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False,methods=['GET'],url_name='getStatus',url_path='status')
    def getStatus(self,request,*args,**kwargs):
        user = request.user
        return Response({"is_hidden":user.is_hidden,"is_staff":user.is_staff})

    @action(detail=False,methods=['POST'],url_name='sendVerifyEmail',url_path='send_verify_email')
    def sendVerifyEmail(self,request,*args,**kwargs):
        user = request.user
        if user.is_verified:
            return Response({"detail":"Already Verified."},status=status.HTTP_208_ALREADY_REPORTED)
        serializer = self.get_serializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            current_site = get_current_site(request)
            utils.sendRegisterValidationEmail(user,current_site=current_site)
            return Response({"detail":"Email Sent."})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            username = request.user.username
            password = request.data['old_password']
        except KeyError:
            return Response({"detail":"Password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = auth.authenticate(username=username, password=password)
        
        if user is None:
            return Response({"detail":"Wrong Password"}, status=status.HTTP_400_BAD_REQUEST)
        
        #if not user.is_verified:
        #    return Response({"detail":"Please Verify your email first."}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('new_password',None)

        if new_password:
            if len(new_password) >= 8:
                user.set_password(new_password)
            else: 
                return Response({"detail":"New Password too short"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.save()
        serializer = serializers.UserDetailUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

class AdminUserViewSet(viewsets.ModelViewSet):
    """
    User viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = UserModel.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminUser]
    serializer_class = serializers.UserFullSerializer
    
    def update(self,request,*args,**kwargs):
        user = self.get_object()
        new_password = request.data.get('new_password',None)
        if new_password:
            if len(new_password) >= 8:
                user.set_password(new_password)
                user.save()
            else:
                return Response({"detail":"New Password too short"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.UserFullSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)