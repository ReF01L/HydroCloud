from django.db import models
from django.utils.translation import gettext_lazy as _

VOLUMETRIC_SCATTER_FILTERING = 'Volumetric Scatter Filtering'
MEDIAN_FILTERING = 'Median Filtering'
DOUBLE_FILTERING = 'Double Filtering'
LOGARITHMIC_FILTERING = 'Logarithmic Filtering'


class Algorithms(models.TextChoices):
    VolumetricScatterFiltering = VOLUMETRIC_SCATTER_FILTERING, _('Фильтрации объёмного рассеяния')
    MedianFiltering = MEDIAN_FILTERING, _('Медианная фильтрация')
    DoubleFiltering = DOUBLE_FILTERING, _('Двойная фильтрация')
    LogarithmicFiltering = LOGARITHMIC_FILTERING, _('Логарифмическая фильтрация')


class Statuses(models.TextChoices):
    InProcess = 'In process', _('В процессе')
    Complete = 'Complete', _('Готов')


def get_volumetric_scatter_filtering_dict(params):
    return {
        'mu': params[0]
    }


def get_median_filtering_dict(params):
    return {
        'window_size': params[0]
    }


def get_double_filtering_dict(params):
    return {
        'mu': params[0]
    }


def get_logarithmic_filtering_dict(params):
    return {
        'a': params[0]
    }
