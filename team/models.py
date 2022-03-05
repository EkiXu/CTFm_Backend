from datetime import datetime
from django.db import models
from django.db.models.aggregates import Sum
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save

from challenge.models import Challenge,SolutionDetail

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=64,unique=True)
    token = models.CharField(max_length=64,unique=True)
    avatar_url = models.CharField(max_length=256)
    description = models.CharField(max_length=512)

    #取消leader到Team的反查
    leader = models.ForeignKey("user.User",null=True,default=None,on_delete=models.SET_NULL,related_name='+')

    attempted_challenges = models.ManyToManyField(Challenge, through='challenge.SolutionDetail')

    @property
    def points(self) -> float:
        value = 0
        all_solved_challenge = SolutionDetail.objects.filter(team=self).filter(solved=True).filter(user__is_hidden=False).filter(challenge__is_hidden=False).filter(challenge__is_hidden=False)
        solved_challenge:SolutionDetail
        for solved_challenge in all_solved_challenge:
            value = value+ solved_challenge.challenge.points
        return value

    @property
    def members(self):
        data = self.user_set.all()
        members = []
        for user in data:
            userInfo = {
                "id":user.pk,
                "nickname":user.nickname,
                "points":user.points,
            }
            members.append(userInfo)
        return members
    @property
    def member_amount(self):
        amount = self.user_set.all().count()
        return amount

    @property
    def solved_amount(self) -> int:
        amount = SolutionDetail.objects.filter(team = self).filter(solved=True).filter(user__is_hidden=False).filter(challenge__is_hidden=False).count()
        return amount

    @property
    def solved_challenges(self) -> int:
        challenges = SolutionDetail.objects.filter(team = self).filter(solved=True).filter(user__is_hidden=False).filter(challenge__is_hidden=False).values("challenge","pub_date")
        return challenges

    @property
    def attempt_amount(self) -> int:
        amount = SolutionDetail.objects.filter(team = self).aggregate(nums=Sum('times'))
        return amount

def change_team_rank_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set("team_rank_updated_at", datetime.utcnow())

post_save.connect(receiver=change_team_rank_updated_at, sender=Team)
post_delete.connect(receiver=change_team_rank_updated_at, sender=Team)



