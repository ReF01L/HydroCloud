from django.conf import settings
from django.db import models

from account import consts


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(default='0000', max_length=4)

    def __str__(self):
        return self.user.username


class Algorithm(models.Model):
    user = models.ForeignKey(to=Profile, on_delete=models.CASCADE, verbose_name='Username')
    name = models.CharField(choices=consts.Algorithms.choices, max_length=50, verbose_name='Algorithm name')
    params = models.CharField(max_length=1000, verbose_name='Parameters')
    image = models.ImageField(upload_to='algs', default='')
    slug = models.SlugField(unique=True)
    status = models.CharField(choices=consts.Statuses.choices, max_length=50, verbose_name='Status', default=consts.Statuses.choices[0])
    file = models.FileField(upload_to='jsf', default=None)

    def __str__(self):
        return self.name
