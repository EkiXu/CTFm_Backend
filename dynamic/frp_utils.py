# Refer CTFd_Whale

import requests

from dynamic.db_utils import DBUtils
from challenge.models import Challenge
from dynamic import models

class FrpUtils:
    @staticmethod
    def update_frp_redirect():
        configs = DBUtils.get_all_configs()
        domain = configs.get('frp_http_domain_suffix', "")

        containers = DBUtils.get_all_alive_container()

        output = configs.get("frp_config_template")

        http_template = "\n\n[http_%s]\n" + \
                        "type = http\n" + \
                        "local_ip = %s\n" + \
                        "local_port = %s\n" + \
                        "custom_domains = %s\n" + \
                        "use_compression = true"

        direct_template = "\n\n[direct_%s]\n" + \
                          "type = tcp\n" + \
                          "local_ip = %s\n" + \
                          "local_port = %s\n" + \
                          "remote_port = %s\n" + \
                          "use_compression = true" + \
                          "\n\n[direct_%s_udp]\n" + \
                          "type = udp\n" + \
                          "local_ip = %s\n" + \
                          "local_port = %s\n" + \
                          "remote_port = %s\n" + \
                          "use_compression = true"
        c:models.ChallengeContainer
        for c in containers:
            dynamic_docker_challenge:Challenge = c.challenge

            if dynamic_docker_challenge.protocol == Challenge.HTTP:
                output += http_template % (
                    str(c.user_id) + '-' + str(c.uuid), str(c.user_id) + '-' + str(c.uuid),
                    dynamic_docker_challenge.redirect_port, c.uuid + domain)
            elif dynamic_docker_challenge.protocol == Challenge.TCP:
                output += direct_template % (
                    str(c.user_id) + '-' + str(c.uuid), str(c.user_id) + '-' + str(c.uuid),
                    dynamic_docker_challenge.redirect_port, c.port,
                    str(c.user_id) + '-' + str(c.uuid), str(c.user_id) + '-' + str(c.uuid),
                    dynamic_docker_challenge.redirect_port, c.port)

        requests.put("http://" + configs.get("frp_api_ip") + ":" + configs.get("frp_api_port") + "/api/config", output,
                     timeout=5)
        
        requests.get("http://" + configs.get("frp_api_ip") + ":" + configs.get("frp_api_port") + "/api/reload", timeout=5)
        