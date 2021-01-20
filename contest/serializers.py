from rest_framework import serializers
from contest.models import Contest
from django.contrib.auth import get_user_model

class ContestSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['start_time'] > data['end_time']:
            raise serializers.ValidationError("end_time must occur after start_time")
        return data
    class Meta:
        model = Contest
        fields = "__all__"

UserModel = get_user_model()

class ScoreboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id","nickname","solved_amount","points","last_point_at","solved_challenges")
        read_only_field = [
            "id",
            "nickname",
            "solved_amount",
            "points",
            "last_point_at"
        ]
        ordering = ['points']
