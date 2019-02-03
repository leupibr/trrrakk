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

    def test_round_time(self):
        actual = datetime(day=10, month=2, year=2019, hour=10, minute=21)
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=10, minute=30),
                         TimeRecord.round_time(actual, timedelta(minutes=30)))
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=10, minute=15),
                         TimeRecord.round_time(actual, timedelta(minutes=15)))
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=10, minute=20),
                         TimeRecord.round_time(actual, timedelta(minutes=10)))
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=10, minute=20),
                         TimeRecord.round_time(actual, timedelta(minutes=5)))

        actual = datetime(day=10, month=2, year=2019, hour=10, minute=53)
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=11, minute=00),
                         TimeRecord.round_time(actual, timedelta(minutes=30)))
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=11, minute=00),
                         TimeRecord.round_time(actual, timedelta(minutes=15)))
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=10, minute=50),
                         TimeRecord.round_time(actual, timedelta(minutes=10)))
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=10, minute=55),
                         TimeRecord.round_time(actual, timedelta(minutes=5)))

