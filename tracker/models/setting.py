import enum

from django.contrib.auth import get_user_model
from django.db import models
from timezone_field import TimeZoneField

from django.conf.locale import LANG_INFO


class DurationFormat(enum.IntEnum):
    CLASSIC = 1
    DECIMAL = 2


class Setting(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    timezone = TimeZoneField(default='UTC')
    locale = models.CharField(
        max_length=10,
        choices=[(li['code'], li['name_local']) for li in LANG_INFO.values() if not li.get('fallback')],
        default='en'
    )

    duration_format = models.PositiveSmallIntegerField(
        choices=[
            (DurationFormat.CLASSIC, 'Classic (3:45)'),
            (DurationFormat.DECIMAL, 'Decimal (3.75)'),
        ],
        default=DurationFormat.CLASSIC
    )