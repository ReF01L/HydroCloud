from django.db import models
from django.utils.translation import gettext_lazy as _


class Algorithms(models.TextChoices):
    VolumetricScatterFiltering = 'Volumetric Scatter Filtering', _('Фильтрации объёмного рассеяния')
    MedianFiltering = 'Median Filtering', _('Медианная фильтрация')
    DoubleFiltering = 'Double Filtering', _('Двойная фильтрация')
    LogarithmicFiltering = 'Logarithmic Filtering', _('Логарифмическая фильтрация')


class Statuses(models.TextChoices):
    InProcess = 'In process', _('В процессе')
    Complete = 'Complete', _('Готов')


def get_volumetric_scatter_filtering_dict(params):
    return {
        'mu': params[0]
    }
