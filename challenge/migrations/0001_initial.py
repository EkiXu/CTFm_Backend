# Generated by Django 4.0 on 2021-12-23 12:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default='', max_length=256)),
                ('content', models.TextField(default='')),
                ('author', models.CharField(default='', max_length=256)),
                ('summary', models.CharField(default='', max_length=256)),
                ('initial_points', models.BigIntegerField(default=0)),
                ('minimum_points', models.BigIntegerField(default=0)),
                ('decay', models.BigIntegerField(default=0)),
                ('is_hidden', models.BooleanField(default=True)),
                ('have_dynamic_container', models.BooleanField(default=False)),
                ('attachment_url', models.CharField(max_length=512, null=True)),
                ('flag', models.CharField(default='', max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='ChallengeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.CharField(max_length=512)),
                ('icon', models.CharField(default='', max_length=64)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='SolutionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solved', models.BooleanField(default=False)),
                ('times', models.IntegerField(default=1)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenge.challenge')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
    ]
