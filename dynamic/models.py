import uuid
from datetime import datetime

from django.db import models

from challenge.models import Challenge

class WhaleConfig(models.Model):
    key = models.CharField(primary_key=True,max_length=128)
    value = models.TextField()

class ChallengeContainer(models.Model):
    user = models.ForeignKey("user.User",on_delete=models.CASCADE)
    challenge = models.ForeignKey("challenge.Challenge", on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=datetime.utcnow)
    renew_count = models.IntegerField(null=True,default=0)
    status = models.IntegerField(default=1)
    uuid = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    port = models.IntegerField(null=True,default=0)
    flag = models.CharField(max_length=512,default="")