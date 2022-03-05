# Refer CTFd_Whale
from math import fabs
from user.models import User
from challenge.models import Challenge
from dynamic.db_utils import DBUtils
from dynamic.docker_utils import DockerUtils

from dynamic.redis_utils import RedisUtils
from dynamic.models import ChallengeContainer


class ControlUtil:
    @staticmethod
    def add_user_container(user, challenge, flag, port=0) -> ChallengeContainer:
        container = DBUtils.create_new_container(user, challenge, flag, port)
        #DockerUtils.add_new_docker_container(user=user, challenge=challenge, flag=flag, uuid_code=uuid_code)
        return container

    @staticmethod
    def remove_user_container(user):
        # docker_result = DockerUtils.remove_current_docker_container(user)
        # if docker_result:
        #     container = ControlUtil.get_container(user)
        #     port = container.port
        #     DBUtils.remove_current_container(user)
        #     if port != 0:
        #         redis_util = RedisUtils()
        #         redis_util.add_available_port(port)

        # return docker_result
        return False

    @staticmethod
    def get_user_container(user)->ChallengeContainer:
        return DBUtils.get_user_current_containers(user)

    @staticmethod
    def renew_user_container(user, challenge):
        DBUtils.renew_current_container(user, challenge)
