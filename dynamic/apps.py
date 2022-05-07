from django.apps import AppConfig
from django.db.utils import ProgrammingError

class DynamicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dynamic'
    def ready(self):
        try:
            from dynamic.redis_utils import RedisUtils
            redis_utils = RedisUtils()
            redis_utils.init_redis_port_sets()
        #disable expection before migrations
        except ProgrammingError:
            pass