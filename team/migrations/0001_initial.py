# Generated by Django 4.0 on 2021-12-23 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('challenge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('token', models.CharField(max_length=64, unique=True)),
                ('avatar_url', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=512)),
                ('attempted_challenges', models.ManyToManyField(through='challenge.SolutionDetail', to='challenge.Challenge')),
            ],
        ),
    ]
