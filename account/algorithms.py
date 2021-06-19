from django.db import models
from django.utils.translation import gettext_lazy as _


class Algorithms(models.TextChoices):
    VolumetricScatterFiltering = 'Фильтрации объёмного рассеяния', _('Volumetric Scatter Filtering')
    MedianFiltering = 'Медианная фильтрация', _('Median Filtering')
    DoubleFiltering = 'Двойная фильтрация', _('Double Filtering')
    LogarithmicFiltering = 'Логарифмическая фильтрация', _('Logarithmic Filtering')
