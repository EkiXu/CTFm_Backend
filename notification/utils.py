from datetime import datetime
from django.core.cache import cache
from rest_framework_extensions.key_constructor.bits import (
    KeyBitBase,
    ListSqlQueryKeyBit,
    PaginationKeyBit,
    RetrieveSqlQueryKeyBit,
)
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor

class UpdatedAtKeyBit(KeyBitBase):
    key = "updated_at"

    def get_data(self, **kwargs):
        value = cache.get(self.key, None)
        if not value:
            value = datetime.utcnow()
            cache.set(self.key, value=value)
        return str(value)

class NotificationUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "notification_updated_at"

class NotificationListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = NotificationUpdatedAtKeyBit()

class NotificationObjectKeyConstructor(DefaultKeyConstructor):
    retrieve_sql = RetrieveSqlQueryKeyBit()
    updated_at = NotificationUpdatedAtKeyBit()
