from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from rest_framework import serializers
from challenge.models import Challenge,SolutionDetail,ChallengeCategory

class ChallengeCategorySerializer(serializers.ModelSerializer):
    challenge_amount = serializers.SerializerMethodField()
    class Meta:
        model = ChallengeCategory
        fields = ["id","name","icon","description","challenge_amount","updated_at"]
        read_only_fields = [
            "id","challenge_amount","updated_at"
        ]
    
    def get_challenge_amount(self, obj):
        return obj.challenges.filter(is_hidden=False).count()

class FullChallengeCategorySerializer(ChallengeCategorySerializer):
    challenge_amount = serializers.SerializerMethodField()
    
    def get_challenge_amount(self, obj):
        return obj.challenges.count()
    

class FullChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'
        read_only_fields = [
            "id",
            "solved_amount",
            "attempt_amount",
            "points",
        ]
        extra_kwargs = {"attachment_url": {"required": False, "allow_null": True,"allow_blank": True},"summary": {"required": False, "allow_null": True,"allow_blank": True}}

class TinyChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['id', 'title','points','solved_amount','attempt_amount']
        read_only_fields = [
            "id",
            "solved_amount",
            "attempt_amount",
            "points"
        ]

class BaseChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['id','category', 'title','summary', 'author','points','solved_amount','attempt_amount','is_hidden']
        read_only_fields = [
            "id",
            "solved_amount",
            "attempt_amount",
            "points"
        ]

class ChallengeSerializer(BaseChallengeSerializer):
    solved = serializers.SerializerMethodField()
    class Meta:
        model = Challenge
        fields = ['id','category', 'title','summary', 'author','points','is_hidden','solved_amount','attempt_amount','solved']
        read_only_fields = [
            "id",
            "solved_amount",
            "attempt_amount",
            "solved",
            "points"
        ]

    def get_solved(self,obj):
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            return None
        try:
            detail = SolutionDetail.objects.get(challenge = obj, user = current_user,solved = True)
            return True
        except ObjectDoesNotExist:
            return False

class ChallengeDetailSerializer(ChallengeSerializer):
    class Meta:
        model = Challenge
        fields = ['id', 'title','content','author','attachment_url','has_dynamic_container']
        read_only_fields = [
            "id",
        ]

class FlagSerializer(serializers.Serializer):
    flag = serializers.CharField(max_length=512)