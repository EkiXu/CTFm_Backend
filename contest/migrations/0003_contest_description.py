# Generated by Django 3.1.3 on 2021-01-18 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_auto_20210104_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='description',
            field=models.TextField(null=True),
        ),
    ]