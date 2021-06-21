from django.db import models
from django.utils.translation import gettext_lazy as _

delimiter = '|'


class Algorithms(models.TextChoices):
    VolumetricScatterFiltering = 'Volumetric Scatter Filtering', _('Фильтрации объёмного рассеяния')
    MedianFiltering = 'Median Filtering', _('Медианная фильтрация')
    DoubleFiltering = 'Double Filtering', _('Двойная фильтрация')
    LogarithmicFiltering = 'Logarithmic Filtering', _('Логарифмическая фильтрация')
