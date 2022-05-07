from rest_framework import serializers
from contest import models

from user.models import User,Team

class ContestSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['start_time'] > data['end_time']:
            raise serializers.ValidationError("end_time must occur after start_time")
        return data
    class Meta:
        model = models.Contest
        fields = "__all__"


class ContestConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContestConfig
        fields = ("key","value")

class ScoreboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","nickname","solved_amount","points","last_point_at","solved_challenges")
        read_only_field = [
            "id",
            "nickname",
            "solved_amount",
            "points",
            "last_point_at"
        ]
        ordering = ['points']

class TeamScoreboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id","name","avatar_url","solved_amount","points","solved_challenges")
        read_only_field = [
            "id",
            "name",
            "avatar_url",
            "solved_amount",
            "points",
        ]
        ordering = ['points']