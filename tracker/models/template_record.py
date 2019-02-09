from django.db import models

from tracker.models import Template
from tracker.models import Project


class TemplateRecord(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
