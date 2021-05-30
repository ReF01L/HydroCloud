from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='img/users/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'
