# Generated by Django 3.1.3 on 2021-01-04 09:19

from django.db import migrations

def forwards_func(apps, schema_editor):
    Contest = apps.get_model("contest", "Contest")
    db_alias = schema_editor.connection.alias
    Contest.objects.using(db_alias).bulk_create([
        Contest(name="CTFm"),
    ])


def reverse_func(apps, schema_editor):
    Contest = apps.get_model("contest", "Contest")
    db_alias = schema_editor.connection.alias
    Contest.objects.using(db_alias).filter(name="CTFm").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]