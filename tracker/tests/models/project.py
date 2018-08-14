from datetime import timedelta, datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from tracker.models import TimeRecord, Organization
from tracker.models.project import format_timespan, Project


class ProjectModelTests(TestCase):
    def setUp(self):
        self.user = User()
        self.user.save()

        self.org = Organization(name='MyOrganization')
        self.org.save()

        self.subject = Project(name='MyProject', organization=self.org)
        self.subject.save()

    def test_format_timespan(self):
        self.assertEqual('a moment', format_timespan(timedelta(seconds=1)))
        self.assertEqual('a minute', format_timespan(timedelta(minutes=1)))
        self.assertEqual('59 minutes', format_timespan(timedelta(minutes=59)))
        self.assertEqual('one hour', format_timespan(timedelta(hours=1)))
        self.assertEqual('23 hours', format_timespan(timedelta(hours=23)))
        self.assertEqual('one day', format_timespan(timedelta(days=1)))
        self.assertEqual('29 days', format_timespan(timedelta(days=29)))
        self.assertEqual('one month', format_timespan(timedelta(days=30)))
        self.assertEqual('11 months', format_timespan(timedelta(days=30*11)))
        self.assertEqual('one year', format_timespan(timedelta(days=365)))
        self.assertEqual('2 years', format_timespan(timedelta(days=365*2)))
        self.assertEqual('25 years', format_timespan(timedelta(days=365*25)))

    def test_last_updated(self):
        record = TimeRecord(project=self.subject, user=self.user)
        record.start_time = datetime.now(tz=timezone.utc) - timedelta(hours=1)
        record.end_time = datetime.now(tz=timezone.utc)
        record.save()

        self.subject.timerecord_set.add(record)
        self.subject.save()

        self.assertEqual('Last updated a moment ago', self.subject.last_updated())

    def test_last_updated_no_updates(self):
        self.assertEqual('Never updated', self.subject.last_updated())

    def test_last_updated_only_start(self):
        record = TimeRecord(project=self.subject, user=self.user)
        record.start_time = datetime.now(tz=timezone.utc) - timedelta(hours=1)
        record.save()

        self.subject.timerecord_set.add(record)
        self.subject.save()

        self.assertEqual('Never updated', self.subject.last_updated())

    def test_is_tracking_active_record(self):
        record = TimeRecord(project=self.subject, user=self.user)
        record.start_time = datetime.now(tz=timezone.utc) - timedelta(hours=1)
        record.save()

        self.subject.timerecord_set.add(record)
        self.subject.save()

        self.assertIs(True, self.subject.is_tracking(self.user))

    def test_is_tracking_no_entry(self):
        self.assertIs(False, self.subject.is_tracking(self.user))

    def test_is_tracking_no_active_record(self):
        record = TimeRecord(project=self.subject, user=self.user)
        record.start_time = datetime.now(tz=timezone.utc) - timedelta(hours=1)
        record.end_time = datetime.now(tz=timezone.utc)
        record.save()

        self.subject.timerecord_set.add(record)
        self.subject.save()

        self.assertIs(False, self.subject.is_tracking(self.user))

    def test_is_member_none(self):
        self.assertIs(False, self.subject.is_member(self.user))

    def test_is_member_admin(self):
        self.subject.admins.add(self.user)
        self.subject.save()

        self.assertIs(True, self.subject.is_member(self.user))

    def test_is_member_editor(self):
        self.subject.editors.add(self.user)
        self.subject.save()

        self.assertIs(True, self.subject.is_member(self.user))
