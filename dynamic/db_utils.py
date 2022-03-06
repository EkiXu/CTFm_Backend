import uuid
from dynamic import models

class DBUtils:
    @staticmethod
    def get_all_configs():
        configs = models.WhaleConfig.objects.all()
        result = {}

        for c in configs:
            result[str(c.key)] = str(c.value)

        return result

    @staticmethod
    def create_challenge_container(user,challenge,address,port,flag)->models.ChallengeContainer:
        uuid_code = uuid.uuid4()
        container = models.ChallengeContainer(user=user, challenge=challenge, flag=flag, uuid=uuid_code,address=address, port=port)
        container.save()
        return container
    
    @staticmethod
    def get_user_challenge_container(user,challenge)->models.ChallengeContainer:
        container:models.ChallengeContainer = models.ChallengeContainer.objects.get(user=user,challenge=challenge)
        return container

    @staticmethod
    def drop_user_container(user,challenge=None) -> bool:
        container: models.ChallengeContainer
        query = models.ChallengeContainer.objects.filter(user=user)
        if challenge!=None:
            query = query.filter(challenge=challenge)
        records = query.all()

        for container in records:
            container.delete()
        return True

    @staticmethod
    def renew_user_container(user,challenge,start_time=None) -> models.ChallengeContainer:
        container:models.ChallengeContainer = models.ChallengeContainer.objects.get(user=user,challenge=challenge)
        container.start_time = start_time
        container.renew_count += 1
        container.save()

