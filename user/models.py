from datetime import datetime
from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.aggregates import Sum
from django.db.models.signals import post_delete, post_save
from team.models import Team
from challenge.models import Challenge,SolutionDetail
from dynamic.models import ChallengeContainer

class User(AbstractUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50,unique=True,blank=True)
    last_point_at = models.DateTimeField(null=True, blank=True, default=None)
    is_hidden = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    team = models.ForeignKey(Team,default=None,null=True, on_delete=models.SET_NULL)

    attempted_challenges = models.ManyToManyField(Challenge, through='challenge.SolutionDetail')

    @property
    def points(self) -> float:
        value = 0
        all_solved_challenge = SolutionDetail.objects.filter(user=self).filter(solved=True).filter(challenge__is_hidden=False)
        solved_challenge:SolutionDetail
        for solved_challenge in all_solved_challenge:
            value = value + solved_challenge.challenge.points
        return value

    @property
    def solved_amount(self) -> int:
        amount = SolutionDetail.objects.filter(user = self).filter(solved=True).filter(challenge__is_hidden=False).count()
        return amount

    @property
    def solved_challenges(self) -> int:
        challenges = SolutionDetail.objects.filter(user = self).filter(solved=True).values("challenge","pub_date")
        return challenges

    @property
    def attempt_amount(self) -> int:
        amount = SolutionDetail.objects.filter(user = self).aggregate(nums=Sum('times'))
        return amount

    @property
    def container_count(self):
        count = ChallengeContainer.objects.filter(user = self).count()
        return count


def change_rank_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set("rank_updated_at", datetime.utcnow())

post_save.connect(receiver=change_rank_updated_at, sender=User)
post_delete.connect(receiver=change_rank_updated_at, sender=User)
    
