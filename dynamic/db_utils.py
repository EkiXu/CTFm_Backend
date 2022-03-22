from signal import raise_signal
from statistics import mode
from typing import List
import uuid
from dynamic import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

class DBUtils:
    @staticmethod
    def get_all_configs():
        configs = models.WhaleConfig.objects.all()
        result = {}

        for c in configs:
            result[str(c.key)] = str(c.value)

        return result

    @staticmethod
    def get_config(key:str,default:str=None):
        value:str 
        try:
            value = models.WhaleConfig.objects.get(key=key).value
        except ObjectDoesNotExist as e:
            if default!=None:
                return default
            else:
                raise e
        return value

    @staticmethod
    def create_challenge_container(user_id,challenge_id,port,flag)->models.ChallengeContainer:
        container = models.ChallengeContainer(user_id=user_id, challenge_id=challenge_id, flag=flag, uuid=uuid.uuid4(),port=port)
        container.save()
        return container
    
    @staticmethod
    def get_user_challenge_container(user_id,challenge_id)->models.ChallengeContainer:
        query = models.ChallengeContainer.objects.get_queryset()
        container:models.ChallengeContainer
        try:
            container = query.get(user_id=user_id,challenge_id=challenge_id)
        except:
            return None
        return container

    @staticmethod
    def drop_user_challenge_container(user_id,challenge_id=None) -> bool:
        container: models.ChallengeContainer
        query = models.ChallengeContainer.objects.filter(user_id=user_id)
        if challenge_id!=None:
            query = query.filter(challenge_id=challenge_id)
        records = query.all()

        for container in records:
            container.delete()
        return True

    @staticmethod
    def renew_user_challenge_container(user_id,challenge_id,start_time=None) -> models.ChallengeContainer:
        container:models.ChallengeContainer = models.ChallengeContainer.objects.get(user_id=user_id,challenge_id=challenge_id)
        if start_time != None:
            container.start_time = start_time
        container.start_time = timezone.now()
        container.renew_count += 1
        container.save()
        return container

    @staticmethod
    def get_all_container() -> List[models.ChallengeContainer]:
        query = models.ChallengeContainer.objects.get_queryset()
        return query.all()

    @staticmethod
    def get_all_container_count() -> int:
        query =  models.ChallengeContainer.objects.get_queryset()
        query = query.all()
        return query.count()

    @staticmethod
    def get_all_alive_container():
        configs = DBUtils.get_all_configs()
        timeout = int(configs.get("docker_timeout", "3600"))

        query  = models.ChallengeContainer.objects.get_queryset()
        query  = query.filter(start_time__gte = timezone.now() - timezone.timedelta(seconds=timeout))
        return query.all()
    
    @staticmethod
    def get_all_alive_container_count():
        configs = DBUtils.get_all_configs()
        timeout = int(configs.get("docker_timeout", "3600"))

        query = models.ChallengeContainer.objects.get_queryset()
        query = query.filter(start_time__gte = timezone.now() - timezone.timedelta(seconds=timeout))
        return query.count()

    @staticmethod
    def get_all_expired_container():
        configs = DBUtils.get_all_configs()
        timeout = int(configs.get("docker_timeout", "3600"))

        query = models.ChallengeContainer.objects.get_queryset()
        query = query.filter(start_time__lt = timezone.now() - timezone.timedelta(seconds=timeout))
        return query.all()

