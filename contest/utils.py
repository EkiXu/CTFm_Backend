import functools
from datetime import datetime
from django.utils import timezone
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework_extensions.key_constructor.bits import (
    KeyBitBase,
    PaginationKeyBit,
)
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor

from contest import models


class UpdatedAtKeyBit(KeyBitBase):
    key = "updated_at"
    def get_data(self, **kwargs):
        value = cache.get(self.key, None)
        if not value:
            value = datetime.utcnow()
            cache.set(self.key, value=value)
        return str(value)

class RankUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "rank_updated_at"

class ContestUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "contest_updated_at"

class ContestKeyConstructor(DefaultKeyConstructor):
    updated_at = ContestUpdatedAtKeyBit()

class ScoreboardKeyConstructor(DefaultKeyConstructor):
    pagination = PaginationKeyBit()
    updated_at = RankUpdatedAtKeyBit()

class TopTenTrendKeyConstructor(DefaultKeyConstructor):
    updated_at = RankUpdatedAtKeyBit()

def IsAfterContest():
    current_time = timezone.now()
    try:
        contest = models.Contest.objects.first()
        return current_time > contest.end_time 
    except (ObjectDoesNotExist,TypeError):
        return True

def IsBeforeContest():
    current_time = timezone.now()
    try:
        contest = models.Contest.objects.first()
        return  current_time < contest.start_time
    except (ObjectDoesNotExist,TypeError):
        return True

def contest_began_or_forbbiden(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        if IsBeforeContest():
            return Response({"detail":"Contest has not yet started"},status=status.HTTP_423_LOCKED)
        return func(*args, **kw)
    return wrapper

def in_contest_time_or_forbbiden(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        if IsBeforeContest():
            return Response({"detail":"Contest has not yet started"},status=status.HTTP_423_LOCKED)
        if IsAfterContest():
            return Response({"detail":"Contest is over"},status=status.HTTP_423_LOCKED)
        return func(*args, **kw)
    return wrapper


def get_all_contest_configs():
    configs = models.ContestConfig.objects.all()
    result = {}

    for c in configs:
        result[str(c.key)] = str(c.value)

    return result

def get_contest_config_value(key:str,default:str=None):
    
    config:models.ContestConfig 
    try:
        config = models.ContestConfig.objects.get(key=key)
    except ObjectDoesNotExist as e:
        if default!=None:
            return default
        else:
            raise e
    return config.value
        
