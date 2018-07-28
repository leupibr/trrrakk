from django.contrib.auth import get_user_model
from django.db import models

from tracker.models import Organization


class Project(models.Model):
    name = models.CharField(max_length=200)

    admins = models.ManyToManyField(get_user_model(), related_name='administrated_projects', verbose_name='Administrators')
    editors = models.ManyToManyField(get_user_model(), blank=True, related_name='editable_projects')

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.name, self.organization.name)