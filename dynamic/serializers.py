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
            'address':instance.address,
            'protocol': instance.challenge.protocol,
            'port': instance.port,
            'user': instance.user.id,
            'challenge': instance.challenge.id,
            'status': instance.status,
            'start_time':instance.start_time,
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