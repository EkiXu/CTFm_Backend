
from django.db.models.aggregates import Count,Sum
from django.db import models
from user.models import BaseUser

# Create your models here.
class ChallengeCategory(models.Model):
    name = models.CharField(max_length=64,unique=True)
    description = models.CharField(max_length=512)
    icon = models.CharField(max_length=256,default="")
    updated_at = models.DateTimeField(auto_now=True)

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

    flag = models.CharField(max_length=512,default="")

    category = models.ForeignKey(
        ChallengeCategory,related_name='challenges',on_delete=models.CASCADE)

    @property
    def attempt_amount(self):
        amount = SolutionDetail.objects.filter(challenge = self).aggregate(nums=Sum('times'))
        if amount['nums'] == None:
            return 0
        return amount['nums']
    @property
    def solved_amount(self):
        amount = SolutionDetail.objects.filter(challenge = self).filter(solved=True).count()
        return amount
    
    @property
    def points(self):
        if self.decay == 0:
            return self.initial_points
        value = (
            ((self.minimum_points - self.initial_points) / (self.decay ** 2))
            * (self.solved_amount ** 2)
        ) + self.initial_points
        return value

class ContestUser(BaseUser):
    @property
    def points(self):
        value = 0
        all_solved_challenge = SolutionDetail.objects.filter(user=self).filter(solved=True)
        for solved_challenge in all_solved_challenge:
            value = value+ solved_challenge.challenge.points
        return value

    @property
    def solved_amount(self):
        amount = SolutionDetail.objects.filter(user = self).filter(solved=True).count()
        return amount
    @property
    def attempt_amount(self):
        amount = SolutionDetail.objects.filter(user = self).aggregate(nums=Sum('times'))
        return amount


class SolutionDetail(models.Model):
    challenge = models.ForeignKey(Challenge,on_delete=models.CASCADE)
    user = models.ForeignKey(ContestUser,on_delete=models.CASCADE)
    solved = models.BooleanField(default=False)
    times = models.IntegerField(default=1)
    pub_date = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering=['-pub_date']