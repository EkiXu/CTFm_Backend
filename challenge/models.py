from django.db import models
from user.models import User

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
    
    difficulty = models.IntegerField(default=0)
    initial_points = models.BigIntegerField(default=0)
    minimum_points = models.BigIntegerField(default=0)
    decay = models.BigIntegerField(default=0)

    flag = models.CharField(max_length=512,default="")

    category = models.ForeignKey(
        ChallengeCategory,related_name='challenges',on_delete=models.CASCADE)

    @property
    def solved_amount(self):
        amount = SolutionDetail.objects.filter(challenge = self).count()
        return amount

    @property
    def points(self):
        if self.decay == 0:
            return self.initial_points
        value = (
            ((self.initial_points - self.minimum_points) / (self.decay ** 2))
            * (self.solved_amount ** 2)
        ) + self.minimum_points
        return value

class SolutionDetail(models.Model):
    challenge = models.ForeignKey(Challenge,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering=['-pub_date']
