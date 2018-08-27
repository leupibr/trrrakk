from datetime import datetime, timedelta

from django.test import TestCase

from tracker.models import TimeRecord


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