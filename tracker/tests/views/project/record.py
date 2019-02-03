from django.test import TestCase

from tracker.views.project.record import *


class RecordTests(TestCase):
    def test_round_time(self):
        actual = datetime(day=10, month=2, year=2019, hour=10, minute=21)
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=10, minute=30),
                         round_time(actual, timedelta(minutes=30)))
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=10, minute=15),
                         round_time(actual, timedelta(minutes=15)))
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=10, minute=20),
                         round_time(actual, timedelta(minutes=10)))
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=10, minute=20),
                         round_time(actual, timedelta(minutes=5)))

        actual = datetime(day=10, month=2, year=2019, hour=10, minute=53)
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=11, minute=00),
                         round_time(actual, timedelta(minutes=30)))
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=11, minute=00),
                         round_time(actual, timedelta(minutes=15)))
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=10, minute=50),
                         round_time(actual, timedelta(minutes=10)))
        self.assertEqual(datetime(day=10, month=2, year=2019, hour=10, minute=55),
                         round_time(actual, timedelta(minutes=5)))
