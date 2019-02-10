from django.conf.locale import LANG_INFO
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import BooleanField
from timezone_field import TimeZoneField


class Setting(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    timezone = TimeZoneField(default='UTC')

    LOCALES = [(li['code'], li['name_local']) for li in LANG_INFO.values() if not li.get('fallback')]
    locale = models.CharField(
        max_length=10,
        choices=LOCALES,
        default='en'
    )

    DURATION_FORMAT_CLASSIC = 1
    DURATION_FORMAT_DECIMAL = 2
    DURATION_FORMATS = [
        (DURATION_FORMAT_CLASSIC, 'Classic (3:45)'),
        (DURATION_FORMAT_DECIMAL, 'Decimal (3.75)'),
    ]
    duration_format = models.PositiveSmallIntegerField(
        choices=DURATION_FORMATS,
        default=DURATION_FORMAT_CLASSIC
    )

    allow_parallel_tracking = BooleanField(default=False)

    ROUNDING_1MIN = 1
    ROUNDING_5MIN = 5
    ROUNDING_10MIN = 10
    ROUNDING_15MIN = 15
    ROUNDING_30MIN = 30
    ROUNDING_VALUES = [
        (ROUNDING_1MIN, 'No rounding'),
        (ROUNDING_5MIN, '5 minutes'),
        (ROUNDING_10MIN, '10 minutes'),
        (ROUNDING_15MIN, '15 minutes'),
        (ROUNDING_30MIN, '30 minutes')
    ]
    timestamp_rounding = models.PositiveSmallIntegerField(
        choices=ROUNDING_VALUES,
        default=ROUNDING_1MIN
    )

