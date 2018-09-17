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
