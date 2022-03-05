from rest_framework import serializers

from dynamic import models

class WhaleConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WhaleConfig
        fields = ("key","value")

class BaseChallengeContainerSerializer(serializers.BaseSerializer):
    def to_representation(self, instance:models.ChallengeContainer):
        return {
            'uuid': instance.uuid,
            'port': instance.port,
            'user': instance.user,
            'challenge': instance.challenge,
            'status': instance.status,
            'renew_count':instance.renew_count,
        }
class FullChallengeContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChallengeContainer
        fields = ("uuid","challenge","user","port","start_time","renew_count","status","flag")
        read_only_field = [
            "uuid",
            "challenge",
            "user",
            "port",
            "start_time",
            "status",
        ]