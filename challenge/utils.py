from datetime import datetime
from django.core.cache import cache
from rest_framework_extensions.key_constructor.bits import (
    KeyBitBase,
    ListSqlQueryKeyBit,
    PaginationKeyBit,
    RetrieveSqlQueryKeyBit,
)
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor

from contest.models import Contest


class UpdatedAtKeyBit(KeyBitBase):
    key = "updated_at"

    def get_data(self, **kwargs):
        value = cache.get(self.key, None)
        if not value:
            value = datetime.utcnow()
            cache.set(self.key, value=value)
        return str(value)

class ChallengeUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "challenge_updated_at"

class ChallengeListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = ChallengeUpdatedAtKeyBit()

class ChallengeObjectKeyConstructor(DefaultKeyConstructor):
    retrieve_sql = RetrieveSqlQueryKeyBit()
    updated_at = ChallengeUpdatedAtKeyBit()

class ChallengeCategoryUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "challenge_category_updated_at"

class ChallengeCategoryListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = ChallengeCategoryUpdatedAtKeyBit()

class ChallengeCategoryObjectKeyConstructor(DefaultKeyConstructor):
    retrieve_sql = RetrieveSqlQueryKeyBit()
    updated_at = ChallengeCategoryUpdatedAtKeyBit()
