# Generated by Django 3.1.7 on 2021-06-17 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='status',
        ),
    ]
