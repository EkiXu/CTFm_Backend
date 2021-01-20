from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseUser(AbstractUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50, blank=True)
    last_point_at = models.DateTimeField(null=True, blank=True, default=None)
    is_hidden = models.BooleanField(default=False)
