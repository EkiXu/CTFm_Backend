from rest_framework.throttling import UserRateThrottle

class TenPerMinuteUserThrottle(UserRateThrottle):
    rate = '10/min'


class TwentyPerMinuteUserThrottle(UserRateThrottle):
    rate = '20/min'

class ThirtyPerMinuteUserThrottle(UserRateThrottle):
    rate = '30/min'

class ContainerRateThrottle(UserRateThrottle):
    rate = '2/min'