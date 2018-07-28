from django.test import TestCase

from tracker.models import Organization
from tracker.models import TimeRecord
from datetime import datetime, timedelta


class OrganizationModelTests(TestCase):
    def test_is_userspace(self):
        subject = Organization()
        subject.name = '~username'

        self.assertIs(True, subject.is_user_space())

    def test_not_is_userspace(self):
        subject = Organization()
        subject.name = 'Organization'

        self.assertIs(False, subject.is_user_space())


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
