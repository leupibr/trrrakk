from django.contrib import auth
from django.contrib.auth.models import User

from tracker.models.organization import Organization
from tracker.models.profile import Profile
from tracker.models.project import Project
from tracker.models.setting import Setting
from tracker.models.template import Template
from tracker.models.template_record import TemplateRecord
from tracker.models.time_record import TimeRecord


def get_tracking_records(user: User):
    return TimeRecord.objects \
        .filter(user=user) \
        .filter(end_time__isnull=True)


def is_tracking(user: User):
    tracking_records = get_tracking_records(user)
    return len(tracking_records) > 0


auth.models.User.add_to_class('get_tracking_records', get_tracking_records)
auth.models.User.add_to_class('is_tracking', is_tracking)
