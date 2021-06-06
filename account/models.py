from django.conf import settings
from django.db import models


class Profile(models.Model):
    STATUSES = (
        ('User', 'User'),
        ('Dev', 'Developed'),
        ('Admin', 'Admin')
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='img/users/%Y/%m/%d', blank=True, null=True)
    status = models.CharField(choices=STATUSES, max_length=10, default=STATUSES[0])
    code = models.CharField(default='0000', max_length=4)

    def __str__(self):
        return f'Profile for user {self.user.username}'
