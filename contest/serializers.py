from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from contest.models import Contest
from django.contrib.auth import get_user_model
from challenge.models import SolutionDetail


class ContestSerializer(serializers.ModelSerializer):
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
    '''
    def get_solved_challenges(self, obj):
        res = []
        SolutionDetail.objects.filter().filter(solved=True)
        return res
        
    '''