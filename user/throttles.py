from rest_framework.throttling import UserRateThrottle

class TenPerMinuteUserThrottle(UserRateThrottle):
    rate = '10/min'
