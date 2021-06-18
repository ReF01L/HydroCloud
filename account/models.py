from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(default='0000', max_length=4)

    def __str__(self):
        return self.user.username


# Алгоритмы фильтрации объёмного рассеяния
class VolumetricScatterFiltration(models.Model):
    pass


# Медианная фильтрация
class MedianFiltering(models.Model):
    pass


# Двойная фильтрация
class DoubleFiltration(models.Model):
    pass


# Логарифмическая фильтрация
class LogarithmicFiltering(models.Model):
    pass
