
from datetime import datetime
from enum import Flag
from django.db.models.aggregates import Count,Sum
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.core.cache import cache
import django.utils.timezone as timezone

# Create your models here.
class ChallengeCategory(models.Model):
    name = models.CharField(max_length=64,unique=True)
    description = models.CharField(max_length=512)
    icon = models.CharField(max_length=64,default="")
    updated_at = models.DateTimeField(default=timezone.now)

def change_challenge_category_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set("challenge_category_updated_at", datetime.utcnow())

post_save.connect(receiver=change_challenge_category_updated_at, sender=ChallengeCategory)
post_delete.connect(receiver=change_challenge_category_updated_at, sender=ChallengeCategory)

class Challenge(models.Model):
    pub_date = models.DateTimeField(auto_now=True)
    
    title = models.CharField(max_length=256,default="")
    content = models.TextField(default="")
    author = models.CharField(max_length=256,default="")
    summary = models.CharField(max_length=256,default="")
    
    initial_points = models.BigIntegerField(default=0)
    minimum_points = models.BigIntegerField(default=0)
    decay = models.BigIntegerField(default=0)

    is_hidden = models.BooleanField(default=True)
    
    have_dynamic_container = models.BooleanField(default=False)

    attachment_url = models.CharField(max_length=512,null=True)
    flag = models.CharField(max_length=512,default="")

    category = models.ForeignKey(
        ChallengeCategory,related_name='challenges',on_delete=models.CASCADE)

    @property
    def attempt_amount(self) -> int:
        amount = SolutionDetail.objects.filter(challenge = self).filter(user__is_hidden = False).aggregate(nums=Sum('times'))
        if amount['nums'] == None:
            return 0
        return amount['nums']
    @property
    def solved_amount(self) -> int:
        amount = SolutionDetail.objects.filter(challenge = self).filter(user__is_hidden = False).filter(solved=True).count()
        return amount

    @property
    def points(self) -> float:
        if self.decay == 0:
            return self.initial_points
        value = (
            ((self.minimum_points - self.initial_points) / (self.decay ** 2))
            * (self.solved_amount ** 2)
        ) + self.initial_points
        if(value < self.minimum_points):
            value = self.minimum_points 
        return value

def change_challenge_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set("challenge_updated_at", datetime.utcnow())
    instance.category.update_at = models.DateTimeField(default=timezone.now())

post_save.connect(receiver=change_challenge_updated_at, sender=Challenge)
post_delete.connect(receiver=change_challenge_updated_at, sender=Challenge)

post_save.connect(receiver=change_challenge_category_updated_at, sender=Challenge)
post_delete.connect(receiver=change_challenge_category_updated_at, sender=Challenge)    

class SolutionDetail(models.Model):
    challenge:Challenge = models.ForeignKey(Challenge,on_delete=models.CASCADE)
    user = models.ForeignKey("user.User",on_delete=models.CASCADE)
    team = models.ForeignKey("team.Team",default=None,null=True,on_delete=models.SET_NULL)
    solved = models.BooleanField(default=False)
    times = models.IntegerField(default=1)
    pub_date = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering=['-pub_date']
    

class ChallengeDocker():
    challenge = models.ForeignKey(
    Challenge,related_name='docker',on_delete=models.CASCADE)
    TCP = 1
    HTTP = 2
    PROTOCOL_CHOICES = [
        (TCP, 'TCP'),
        (HTTP, 'HTTP'),
    ]
    protocol = models.IntegerField(
        max_length=2,
        choices=PROTOCOL_CHOICES,
        default=TCP,
    )
    image = models.CharField(max_length=512)
    port = models.IntegerField()
    memory_limit = models.CharField(max_length=64, default="128m")
    cpu_limit = models.FloatField(default=0.5)