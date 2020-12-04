from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from rest_framework import serializers
from challenge.models import Challenge,SolutionDetail,ChallengeCategory

from django.contrib.auth import get_user_model

class ChallengeCategorySerializer(serializers.ModelSerializer):
    challenge_amount = serializers.SerializerMethodField()
    class Meta:
        model = ChallengeCategory
        fields = ["id","name","icon","description","challenge_amount","updated_at"]
        read_only_fields = [
            "id","challenge_amount","updated_at"
        ]
    
    def get_challenge_amount(self, obj):
        return obj.challenges.count()
    

class FullChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'
        read_only_fields = [
            "id",
            "solved_amount",
        ]

class ChallengeSerializer(serializers.ModelSerializer):
    solved = serializers.SerializerMethodField()
    #points = serializers.SerializerMethodField()
    #solved_amount = serializers.SerializerMethodField()
    class Meta:
        model = Challenge
        fields = ['id','category', 'title','summary', 'author','difficulty','points','solved_amount','solved']
        read_only_fields = [
            "id",
            "solved_amount",
            "solved",
            "points"
        ]

    def get_solved(self,obj):
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            return None
        try:
            detail = SolutionDetail.objects.get(challenge = obj, user = current_user)
            return True
        except ObjectDoesNotExist:
            return False
    '''
    def get_points(obj):
        return obj.get_points()

    def get_solved_amount(obj):
        return obj.get_solved_amount()
    '''

class ChallengeDetailSerializer(ChallengeSerializer):
    class Meta:
        model = Challenge
        fields = ['id', 'title', 'summary','content','author','difficulty','solved_amount','solved']
        read_only_fields = [
            "id",
            "solved_amount",
            "solved",
        ]

class FlagSerializer(serializers.Serializer):
    flag = serializers.CharField(max_length=512)