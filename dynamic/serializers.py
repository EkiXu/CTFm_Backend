from rest_framework import serializers

from dynamic import models
from dynamic.db_utils import DBUtils
from challenge.models import Challenge

class WhaleConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WhaleConfig
        fields = ("key","value")

class BaseChallengeContainerSerializer(serializers.BaseSerializer):
    def to_representation(self, instance:models.ChallengeContainer):
        host = instance.host
        port = instance.port
        challenge:Challenge = instance.challenge
        if challenge.protocol == Challenge.HTTP:
            host = str(instance.uuid)+DBUtils.get_config("frp_http_domain_suffix")
            port = DBUtils.get_config("frp_http_port")
        else:
            host = DBUtils.get_config("frp_direct_ip_address")
        
        
        return {
            'uuid': str(instance.uuid),
            'host':host,
            'protocol': challenge.protocol,
            'port': port,
            'user': instance.user.id,
            'challenge': challenge.id,
            'status': instance.status,
            'start_time':instance.start_time,
            'timeout': DBUtils.get_config("docker_container_timeout", "3600"),
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