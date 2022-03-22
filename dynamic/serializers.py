from rest_framework import serializers

from dynamic import models
from dynamic.db_utils import DBUtils

class WhaleConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WhaleConfig
        fields = ("key","value")

class BaseChallengeContainerSerializer(serializers.BaseSerializer):
    def to_representation(self, instance:models.ChallengeContainer):
        host = instance.host
        if host == "" or host == None:
            host = DBUtils.get_config("frp_direct_ip_address")
        
        return {
            'uuid': str(instance.uuid),
            'host':host,
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