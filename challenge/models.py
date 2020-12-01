from django.db import models
from user.models import User

# Create your models here.
class ChallengeCategory(models.Model):
    name = models.CharField(max_length=64,unique=True)
    description = models.CharField(max_length=512)
    icon = models.CharField(max_length=256,default="")
    #challenge_amount = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

class Challenge(models.Model):
    pub_date = models.DateTimeField(auto_now=True)
    
    title = models.CharField(max_length=256,default="")
    content = models.TextField(default="")
    author = models.CharField(max_length=256,default="")
    summary = models.CharField(max_length=256,default="")
    
    difficulty = models.IntegerField(default=0)
    points = models.BigIntegerField(default=0)
    solved_amount = models.BigIntegerField(default=0)
    flag = models.CharField(max_length=512,default="")

    category = models.ForeignKey(
        ChallengeCategory,related_name='challenges',on_delete=models.CASCADE)

class SolutionDetail(models.Model):
    challenge = models.ForeignKey(Challenge,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering=['-pub_date']
