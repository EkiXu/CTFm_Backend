from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    points = models.BigIntegerField(default=0)
    solved_amount  = models.BigIntegerField(default=0)
    last_point_at = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        ordering = ['-points']