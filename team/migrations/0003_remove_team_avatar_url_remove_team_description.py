# Generated by Django 4.1.3 on 2023-03-18 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='avatar_url',
        ),
        migrations.RemoveField(
            model_name='team',
            name='description',
        ),
    ]