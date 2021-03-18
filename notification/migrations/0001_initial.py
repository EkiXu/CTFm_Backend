# Generated by Django 3.1.5 on 2021-03-18 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default='', max_length=256)),
                ('content', models.TextField(default='')),
                ('type_icon', models.CharField(default='', max_length=48)),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
    ]
