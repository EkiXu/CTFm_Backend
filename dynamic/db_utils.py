# Refer CTFd_Whale

import datetime
import uuid

from dynamic.models import WhaleConfig, ChallengeContainer


class DBUtils:
    @staticmethod
    def get_all_configs():
        configs = WhaleConfig.objects.all()
        result = {}

        for c in configs:
            result[str(c.key)] = str(c.value)

        return result

    @staticmethod
    def save_all_configs(configs):
        for c in configs:
            record:WhaleConfig = WhaleConfig.objects.get(key=c[0])
            if record:
                record.value = c[1]
                record.save()
            else:
                config = WhaleConfig(key=c[0], value=c[1])
                config.save()

    @staticmethod
    def create_new_container(user, challenge, flag, port=0)->ChallengeContainer:
        uuid_code = uuid.uuid4()
        container = ChallengeContainer(user=user, challenge=challenge, flag=flag, uuid=uuid_code, port=port)
        container.save()

        return container

    @staticmethod
    def get_user_current_containers(user):
        records = ChallengeContainer.objects.filter(user=user).all()
        
        if len(records) == 0:
            return None

        return records[0]

    @staticmethod
    def get_container_by_port(port):
        container = ChallengeContainer.objects.get(port = port)
        return container

    @staticmethod
    def remove_current_container(user):
        records = ChallengeContainer.objects.filter(user=user)
        # records = q.all()
        # for r in records:
        #     pass

        records.delete()

    @staticmethod
    def renew_current_container(user, challenge) -> ChallengeContainer:
        records = ChallengeContainer.objects \
            .filter(user = user) \
            .filter(challenge = challenge) \
            .all()
        if len(records) == 0:
            return

        configs = DBUtils.get_all_configs()
        timeout = int(configs.get("docker_timeout", "3600"))

        container = records[0]
        container.start_time = container.start_time + datetime.timedelta(seconds=timeout)

        if container.start_time > datetime.datetime.now():
            container.start_time = datetime.datetime.now()

        container.renew_count += 1
        container.save()
        return container

    @staticmethod
    def get_all_expired_container():
        configs = DBUtils.get_all_configs()
        timeout = int(configs.get("docker_timeout", "3600"))

        containers = ChallengeContainer.objects.filter(start_time_lt = datetime.datetime.now() - datetime.timedelta(seconds=timeout)).all()
        return containers

    @staticmethod
    def get_all_alive_container():
        configs = DBUtils.get_all_configs()
        timeout = int(configs.get("docker_timeout", "3600"))

        containers = ChallengeContainer.objects.filter(start_time_gte = datetime.datetime.now() - datetime.timedelta(seconds=timeout)).all()
        return containers

    @staticmethod
    def get_all_container():
        containers = ChallengeContainer.objects.all()
        return containers

    @staticmethod
    def get_all_alive_container_count():
        configs = DBUtils.get_all_configs()
        timeout = int(configs.get("docker_timeout", "3600"))

        return ChallengeContainer.objects \
            .filter(start_time_gte = datetime.datetime.now() - datetime.timedelta(seconds=timeout))\
            .count()
