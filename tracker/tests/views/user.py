from django.test import TestCase

from tracker.views.user import *


class UserTests(TestCase):
    def test_begin_of_week(self):
        expected = datetime(day=13, month=8, year=2018)
        input = datetime(day=15, month=8, year=2018, hour=10, minute=15)
        self.assertEqual(expected, begin_of_week(input))

    def test_begin_of_week_from_str(self):
        expected = datetime(day=13, month=8, year=2018)
        self.assertEqual(expected, begin_of_week('2018-08-15'))

    def test_end_of_week(self):
        expected = datetime(day=19, month=8, year=2018)
        input = datetime(day=15, month=8, year=2018, hour=10, minute=15)
        self.assertEqual(expected, end_of_week(input))

    def test_to_hours_float(self):
        self.assertAlmostEqual(0, to_decimal(timedelta()), places=2)
        self.assertAlmostEqual(.5, to_decimal(timedelta(minutes=30)), places=2)
        self.assertAlmostEqual(1.5, to_decimal(timedelta(minutes=90)), places=2)

    def test_get_backward_step(self):
        result = get_backward_step(datetime(day=13, month=8, year=2018))
        self.assertEqual('2018-08-06', result['from'])
        self.assertEqual('2018-08-12', result['to'])

    def test_get_forward_step(self):
        result = get_forward_step(datetime(day=13, month=8, year=2018))
        self.assertEqual('2018-08-20', result['from'])
        self.assertEqual('2018-08-26', result['to'])

