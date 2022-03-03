from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_recaptcha.fields import ReCaptchaV2Field
from django.conf import settings

from user import utils
from user import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("id","nickname","team","is_verified","solved_amount","points","last_point_at")
        read_only_field = [
            "id",
            "nickname",
            "team",
            "solved_amount",
            "email",
            "points",
            "last_point_at",
            "is_verified",
        ]
        ordering = ['points']

class UserDetailSerializer(UserSerializer):
    class Meta:
        model = models.User
        fields = ("id","email","username","nickname","team","is_verified","solved_amount","points")
        read_only_fields = [
            "id",
            "username",
            "email",
            "points",
            "solved_amount",
            "is_verified",
            "team",
        ]

class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields =  ("id","email","username","nickname","team","solved_amount","points","is_hidden","is_staff","is_verified")
        read_only_fields = [
            "id",
            "points",
            "solved_amount"
        ]


class UserDetailUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True,required=False,allow_blank=True)
    old_password = serializers.CharField(write_only=True)
    class Meta:
        model = models.User
        fields = ("id","email","username","nickname","old_password","new_password")
        read_only_fields = [
            "id",
            "username",
        ]

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("email",)

class RegisterSerializer(serializers.ModelSerializer):
    recaptcha = ReCaptchaV2Field()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        attrs.pop("recaptcha")
        return super().validate(attrs)

    def create(self, validated_data):
        if settings.ENABLE_EMAIL_VALIDATION == False:
            user = models.User.objects.create(
                username = validated_data['username'],
                email = validated_data['email'],
                nickname = validated_data['nickname'],
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
        else:
            user = models.User.objects.create(
                username = validated_data['username'],
                email = validated_data['email'],
                nickname = validated_data['nickname'],
                is_verified = False
            )
            user.set_password(validated_data['password'])
            
            current_site = get_current_site(self.context['request'])
            utils.sendRegisterValidationEmail(user,current_site=current_site)
            user.save()
            return user

    class Meta:
        model = models.User
        fields = ("username","email","nickname",'password','recaptcha')
        required = (
            'username',
            'email',
            'nickname',
            'password',
        )

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = user.id
        token['username'] = user.username
        token['nickname'] = user.nickname
        token['is_staff'] = user.is_staff
        token['is_hidden'] = user.is_hidden
        token['is_verified'] = user.is_verified

        return token