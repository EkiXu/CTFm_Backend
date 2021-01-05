from django.db import models
from django.db.models.base import Model

# Create your models here.
class Contest(models.Model):
    name = models.CharField(max_length=50, blank=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)


    