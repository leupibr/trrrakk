from django.contrib.auth import get_user_model
from django.db import models
from timezone_field import TimeZoneField


class Setting(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    timezone = TimeZoneField(default='UTC')