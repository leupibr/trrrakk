from datetime import datetime, timedelta

from django.test import TestCase

from tracker.models import Organization
from tracker.models import TimeRecord
from tracker.models.project import format_timespan


class OrganizationModelTests(TestCase):
    def test_is_userspace(self):
        subject = Organization()
        subject.name = '~username'

        self.assertIs(True, subject.is_user_space())

    def test_not_is_userspace(self):
        subject = Organization()
        subject.name = 'Organization'

        self.assertIs(False, subject.is_user_space())


class ProjectModelTests(TestCase):
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


class TimeRecordModelTests(TestCase):

    def test_duration(self):
        subject = TimeRecord()
        subject.start_time = datetime(2000, 1, 1, 8, 0, 0)
        subject.end_time = datetime(2000, 1, 1, 9, 0, 0)

        self.assertEqual(timedelta(hours=1), subject.duration())

    def test_duration_incomplete(self):
        subject = TimeRecord()
        subject.start_time = datetime(2000, 1, 1, 8, 0, 0)

        self.assertEqual(timedelta(0, 0), subject.duration())
