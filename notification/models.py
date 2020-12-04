from django.db import models

# Create your models here.

class Notification(models.Model):
    pub_date = models.DateTimeField(auto_now=True)
    
    title = models.CharField(max_length=256,default="")
    content = models.TextField(default="")
    type_icon = models.CharField(max_length=48,default="")

    class Meta:
        ordering = ['-pub_date']

