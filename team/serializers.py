from django.http import request
from rest_framework import viewsets
from rest_framework import serializers

from user.models import User

from team import models
from team import utils

class BaseTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ['name','avatar_url','description',"solved_amount","points"]
        read_only_fields = [
            "name",
            "points",
            "solved_amount"
        ]

class DetailedTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ['name','avatar_url','description','leader','token',"solved_amount","points"]
        read_only_fields = [
            "token",
            "name",
            "points",
            "solved_amount"
        ]

class CreateTeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=64)
    description = serializers.CharField(required=False, allow_blank=True, max_length=128)
    avatar_url = serializers.CharField(required=False, allow_blank=True, max_length=128)

    class Meta:
        model = models.Team
        fields = ['name','description','avatar_url','leader']
    
    def create(self, validated_data):
        token = utils.genTeamToken(validated_data.get('name'))
        leader = validated_data.get('leader')
        team = models.Team.objects.create(name=validated_data.get('name'),description=validated_data.get('description'),avatar_url = validated_data.get('avatar_url'),leader = leader,token=token)
        leader.team = team
        leader.save()
        return team

class JoinTeamSerializer(serializers.Serializer):
    token = serializers.CharField(trim_whitespace=True)