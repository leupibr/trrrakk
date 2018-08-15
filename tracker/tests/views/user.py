from datetime import datetime

from django.test import TestCase

from tracker.views.user import begin_of_week, end_of_week


class UserTests(TestCase):
    def test_begin_of_week(self):
        expected = datetime(day=13, month=8, year=2018)
        input = datetime(day=15, month=8, year=2018, hour=10, minute=15)
        self.assertEqual(expected, begin_of_week(input))

    def test_end_of_week(self):
        expected = datetime(day=19, month=8, year=2018)
        input = datetime(day=15, month=8, year=2018, hour=10, minute=15)
        self.assertEqual(expected, end_of_week(input))

