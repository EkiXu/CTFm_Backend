from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseUser(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    last_point_at = models.DateTimeField(null=True, blank=True, default=None)
    is_hidden = models.BooleanField(default=False)
