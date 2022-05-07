# Refer CTFd_Whale
import uuid

from dynamic.db_utils import DBUtils
from dynamic.docker_utils import DockerUtils

from dynamic.redis_utils import RedisUtils
from dynamic import models


class ControlUtils:
    @staticmethod
    def gen_random_flag()->str:
        return "flag{%s}" % uuid.uuid4()
    @staticmethod
    def add_user_container(user_id, challenge_id,flag=None,port=0,host=None) -> models.ChallengeContainer:
        # if user.container_count >= settings.USER_MAX_CONTAINERS:
        #     raise Exception("user max container limited")
        if flag == None:
            flag = ControlUtils.gen_random_flag()

        container:models.ChallengeContainer = DBUtils.create_challenge_container(user_id,challenge_id,port,flag)

        uuid_code = container.uuid
        
        DockerUtils.add_new_docker_container(user_id,challenge_id,flag,uuid_code)

        #DockerUtils.add_new_docker_container(user=user, challenge=challenge, flag=flag, uuid_code=uuid_code)
        return container

    @staticmethod
    def remove_user_challenge_container(user_id,challenge_id):
        container = DBUtils.get_user_challenge_container(user_id,challenge_id)
        if container == None:
            return False
        docker_result = DockerUtils.remove_user_container(user_id,container.uuid)
        
        if docker_result:
            port = container.port
            DBUtils.drop_user_challenge_container(user_id,challenge_id)
            if port != 0:
                redis_util = RedisUtils(user_id)
                redis_util.add_available_port(port)

        return docker_result

    @staticmethod
    def remove_container(container:models.ChallengeContainer):
        user_id = container.user.id
        challenge_id = container.challenge.id
        docker_result = DockerUtils.remove_user_container(user_id,container.uuid)
        if docker_result:
            port = container.port
            DBUtils.drop_user_challenge_container(user_id,challenge_id)
            if port != 0:
                redis_util = RedisUtils(user_id)
                redis_util.add_available_port(port)

        return docker_result

    @staticmethod
    def renew_user_challenge_container(user_id, challenge_id):
        return DBUtils.renew_user_challenge_container(user_id=user_id, challenge_id=challenge_id)

    @staticmethod
    def get_user_challenge_container(user_id,challenge_id)->models.ChallengeContainer:
        return DBUtils.get_user_challenge_container(user_id,challenge_id)


    @staticmethod
    def gen_random_flag():
        return 'flag{%s}' % uuid.uuid4()
