from datetime import datetime
from django.core.cache import cache
from django.db import models
from django.db.models.base import Model
from django.db.models.signals import post_delete, post_save

# Create your models here.
class Contest(models.Model):
    name = models.CharField(max_length=50, blank=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    description = models.TextField(null=True)


def change_contest_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set("contest_updated_at", datetime.utcnow())

post_save.connect(receiver=change_contest_updated_at, sender=Contest)
post_delete.connect(receiver=change_contest_updated_at, sender=Contest)