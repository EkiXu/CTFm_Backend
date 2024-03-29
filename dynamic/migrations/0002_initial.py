# Generated by Django 4.0.3 on 2022-03-22 04:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dynamic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='challengecontainer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='challengecontainer',
            constraint=models.UniqueConstraint(fields=('user', 'challenge'), name='unique_attention'),
        ),
    ]
