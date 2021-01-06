from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from challenge.models import SolutionDetail,Challenge
from django.db.models.functions import Rank

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id","nickname","solved_amount","points","last_point_at")
        read_only_field = [
            "id",
            "nickname",
            "solved_amount",
            "points",
            "last_point_at"
        ]
        ordering = ['points']

class UserDetailSerializer(UserSerializer):
    class Meta:
        model = UserModel
        fields = ("id","email","username","nickname","solved_amount","points")
        read_only_fields = [
            "id",
            "username",
            "points",
            "solved_amount"
        ]

class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields =  ("id","email","username","nickname","solved_amount","points","is_hidden","is_staff")
        read_only_fields = [
            "id",
            "points",
            "solved_amount"
        ]


class UserDetailUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True,required=False,allow_blank=True)
    old_password = serializers.CharField(write_only=True)
    class Meta:
        model = UserModel
        fields = ("id","email","username","nickname","old_password","new_password")
        read_only_fields = [
            "id",
            "username",
        ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            nickname = validated_data['nickname'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = ("username","email","nickname",'password')
        required = (
            'username',
            'email',
            'nickname',
            'password',
        )

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = user.id
        token['username'] = user.username
        token['nickname'] = user.nickname
        token['is_staff'] = user.is_staff
        token['is_hidden'] = user.is_hidden

        return token