from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from rest_framework import serializers
from contest.models import Contest


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = "__all__"