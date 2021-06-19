from django.conf import settings
from django.db import models

from account import algorithms


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(default='0000', max_length=4)

    def __str__(self):
        return self.user.username


class Algorithm(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Username')
    name = models.CharField(choices=algorithms.Algorithms.choices, max_length=50, verbose_name='Algorithm name')
    params = models.CharField(max_length=1000, verbose_name='Parameters')
