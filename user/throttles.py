from rest_framework.throttling import UserRateThrottle

class TwentyPerMinuteUserThrottle(UserRateThrottle):
    rate = '20/min'
