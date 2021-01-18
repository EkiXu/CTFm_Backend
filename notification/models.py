from datetime import datetime
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete, post_save

# Create your models here.


class Notification(models.Model):
    pub_date = models.DateTimeField(auto_now=True)
    
    title = models.CharField(max_length=256,default="")
    content = models.TextField(default="")
    type_icon = models.CharField(max_length=48,default="")

    class Meta:
        ordering = ['-pub_date']

def change_notification_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set("notification_updated_at", datetime.utcnow())

post_save.connect(receiver=change_notification_updated_at, sender=Notification)
post_delete.connect(receiver=change_notification_updated_at, sender=Notification)