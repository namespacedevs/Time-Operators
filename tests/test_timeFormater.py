from time_operators.operators import TimeFormater, TimeZoneChecker
from datetime import datetime
from unittest import TestCase


class TestTimeFormater(TestCase):
    def test_sum_timezone_greater(self):
        now = datetime.now()
        new = TimeFormater().sum_timezone(now, '-03:00')
        print('times: \n{} \n{}'.format(now, new))
        self.assertLess(now, new)

    def test_sum_timezone_less(self):
        now = datetime.now()
        new = TimeFormater.sum_timezone(now, '+03:00')
        print('times: \n{} \n{}'.format(now, new))
        self.assertGreater(now, new)


class TestTimeZoneChecker(TestCase):
    def test_is_day_receive_json(self):
        timezone = '{"timezone":"{\\"value\\":\\"Greenland Standard Time\\",\\"abbr\\":\\"GDT\\",\\"offset\\":-3,' \
                   '\\"isdst\\":true,\\"text\\":\\"(UTC-03:00) Greenland\\",\\"utc\\":[\\"America/Godthab\\"]}"}'
        self.assertIsInstance(TimeZoneChecker.is_day(timezone), bool)
