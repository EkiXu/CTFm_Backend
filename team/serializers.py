from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from user.models import User

from team import models
from team import utils

class BaseTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ['id','name','avatar_url','description',"solved_amount","points"]
        read_only_fields = [
            "id",
            "name",
            "points",
            "solved_amount"
        ]

class DetailedTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ['id','name','avatar_url','description','leader','token',"solved_amount","members","points"]
        read_only_fields = [
            "id",
            "token",
            "name",
            "members",
            "points",
            "solved_amount"
        ]

class CreateTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ['id','name','token','description','avatar_url','leader']
        read_only_fields = [
            "id",
            "token",
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=models.Team.objects.all(),
                fields=['name','leader']
            )
        ]
    
    def create(self, validated_data):
        validated_data["token"] = utils.genRandomTeamToken()
        team = super().create(validated_data)
        leader = team.leader
        leader.team = team
        leader.save()
        return team

class JoinTeamSerializer(serializers.Serializer):
    token = serializers.CharField(trim_whitespace=True)