import datetime

from django.contrib.auth import get_user_model
from django.db import models

from tracker.models import Project


class TimeRecord(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    modification_time = models.DateTimeField(auto_now=True)

    def duration(self):
        if not self.end_time:
            return datetime.timedelta()
        return self.end_time - self.start_time

    @staticmethod
    def round_time(dt: datetime, resolution: datetime.timedelta):
        """
        Rounds a timestamp by a given resolution.
        Function is based on the following answer on stackoverflow: https://stackoverflow.com/a/31005978

        :param dt: Timestamp to round
        :param resolution: Precision of the output
        :return: A new timestamp rounded to the given precision
        """
        round_to = resolution.total_seconds()
        seconds = (dt.replace(tzinfo=None) - dt.min).seconds
        rounding = (seconds + round_to / 2) // round_to * round_to
        return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)
