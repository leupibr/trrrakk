import bisect
import os.path
import random
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from tracker.models import Organization


class Project(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    identifier = models.CharField(max_length=200, null=False, blank=True)

    admins = models.ManyToManyField(get_user_model(), related_name='administrated_projects',
                                    verbose_name='Administrators')
    editors = models.ManyToManyField(get_user_model(), blank=True, related_name='editable_projects')

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def last_updated(self):
        last_time_record = self.timerecord_set \
            .filter(end_time__isnull=False) \
            .order_by('-modification_time') \
            .first()

        if not last_time_record:
            return 'Never updated'

        return 'Last updated {} ago'.format(format_timespan(timezone.now() - last_time_record.modification_time))

    def is_tracking(self, user):
        no_end_time = self.timerecord_set \
            .filter(end_time__isnull=True) \
            .filter(user=user)

        return len(no_end_time) > 0

    def __str__(self):
        return '{} ({})'.format(self.name, self.organization.name)

    @staticmethod
    def random_name():
        return '{} {}'.format(random.choice(ONE), random.choice(TWO))

    def is_admin(self, user):
        return user in self.admins.all()

    def is_member(self, user):
        return user in self.admins.all() or user in self.editors.all()

    @staticmethod
    def recent_projects(user, num=3):
        user_projects = Project.objects \
            .filter(timerecord__user=user) \
            .order_by('-timerecord__modification_time')

        recent_projects = []
        for i in range(num):
            p = user_projects \
                .exclude(id__in=(p.id for p in recent_projects)) \
                .first()
            if not p:
                break
            recent_projects.append(p)
        return recent_projects


location = os.path.dirname(__file__)
ONE = open(os.path.join(location, 'ONE.txt')).readlines()
TWO = open(os.path.join(location, 'TWO.txt')).readlines()

periods = OrderedDict()
periods[59] = 'a moment', 1
periods[60] = 'a minute', 60
periods[60*60-1] = '{:.0f} minutes', 60
periods[60*60] = 'one hour', 60*60
periods[60*60*24-1] = '{:.0f} hours', 60*60
periods[60*60*24] = 'one day', 60*60*24
periods[60*60*24*30-1] = '{:.0f} days', 60*60*24
periods[60*60*24*30] = 'one month', 60*60*24*30
periods[60*60*24*365-1] = '{:.0f} months', 60*60*24*30
periods[60*60*24*365] = 'one year', 60*60*24*365
periods[60*60*24*365*2] = '{:.0f} years', 60*60*24*365


def format_timespan(delta):
    thresholds = list(periods.keys())
    threshold = bisect.bisect_left(thresholds, delta.total_seconds())

    threshold = threshold - 1 if threshold >= len(thresholds) else threshold
    entry = periods[thresholds[threshold]]
    return entry[0].format(delta.total_seconds()//entry[1])
