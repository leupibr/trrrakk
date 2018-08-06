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