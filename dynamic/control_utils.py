# Refer CTFd_Whale
import uuid
from django.conf import settings
from user.models import User
from challenge.models import Challenge
from dynamic.db_utils import DBUtils
from dynamic.docker_utils import DockerUtils

from dynamic.redis_utils import RedisUtils
from dynamic.models import ChallengeContainer


class ControlUtils:
    @staticmethod
    def gen_random_flag()->str:
        return "flag{%s}" % uuid.uuid4()
    @staticmethod
    def add_user_container(user:User, challenge:Challenge, port=0, flag=None) -> ChallengeContainer:
        if user.container_amount >= settings.USER_MAX_CONTAINERS:
            raise Exception("user max container limited")
        if flag == None:
            if challenge.flag != None and challenge.flag != "":
                flag = challenge.flag
            else:
                flag = ControlUtils.gen_random_flag()
        
        #address,port = DockerUtils.add_new_docker_container(user,challenge,flag)
        port="2333"
        address="127.0.0.1"

        container = DBUtils.create_challenge_container(user,challenge,address,port,flag)

        #DockerUtils.add_new_docker_container(user=user, challenge=challenge, flag=flag, uuid_code=uuid_code)
        return container

    @staticmethod
    def remove_user_container(user:User,challenge:Challenge=None):
        DBUtils.drop_user_container(user,challenge)
        # docker_result = DockerUtils.remove_current_docker_container(user)
        # if docker_result:
        #     container = ControlUtil.get_container(user)
        #     port = container.port
        #     DBUtils.remove_current_container(user)
        #     if port != 0:
        #         redis_util = RedisUtils()
        #         redis_util.add_available_port(port)

        # return docker_result
        return True

    @staticmethod
    def get_user_challenge_container(user:User,challenge:Challenge)->ChallengeContainer:
        return DBUtils.get_user_challenge_container(user,challenge)
    

    @staticmethod
    def renew_user_container(user:User, challenge:Challenge):
        container = DBUtils.renew_user_container(user, challenge)
        return container
