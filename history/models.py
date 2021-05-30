from django.db import models

from account.models import Profile


class History(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    method = models.CharField(max_length=50)
    params = models.TextField(max_length=100)
