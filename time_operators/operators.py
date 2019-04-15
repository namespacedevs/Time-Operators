from datetime import datetime, timedelta

import pytz
import json


def get_ip_timezone(timezone):
    """
    get a account and returns a TimeZone instance
    :param account:
    :return: TimeZone instance
    """
    if timezone is None:
        raise ValueError('get_ip_timezone can\'t receive None')
    try:
        timezone_str = json.loads(timezone)
        timezone_str = json.loads(timezone_str['timezone'])
        timezone_str = timezone_str['text'].split(' ')[0]
        timezone_str = timezone_str.replace('UTC', '')
        timezone_str = timezone_str.replace('(', '')
        timezone_str = timezone_str.replace(')', '')
        if len(timezone_str) <= 5:
            timezone_str = '+00:00'
        try:
            timezone = TimeZone(timezone_str)
        except Exception as e:
            timezone = TimeZone('+00:00')
        return timezone
    except Exception as e:
        raise e


class TimeFormater:
        @staticmethod
        def ensure_timezone(time):
            if time is None:
                raise ValueError('Null time')
            if time.tzinfo is None:
                return pytz.utc.localize(time)
            elif time.tzinfo == pytz.utc:
                return time
            else:
                raise ValueError('that is not a time')

        @staticmethod
        def sum_timezone(time, str_timezone):
            """Get a time on datetime format, and a timezone in str format and sum"""

            if isinstance(str_timezone, TimeZone):
                timezone = str_timezone.time_str
            else:
                timezone = str_timezone
            if timezone is not None:
                if len(timezone) == 6:
                    try:
                        timezone = timezone.split(':')
                        hour = int(timezone[0][1:])
                        minutes = int(timezone[1])
                        signal = timezone[0][0]
                        if signal == '-':
                            delta = timedelta(hours=hour, minutes=minutes)
                            modified = time + delta
                        elif signal == '+':
                            delta = timedelta(hours=hour, minutes=minutes)
                            modified = time - delta
                        else:
                            raise ValueError('the signal of th time is not valid')

                        return modified

                    except Exception as e:
                        raise ValueError('Error: {}'.format(e))
                else:
                    try:
                        tz = get_ip_timezone(timezone)
                        return tz
                    except Exception as e:
                        raise e
            else:
                return time


class TimeLock:
    """Lock database using time rules"""
    def __init__(self, model):
        self.model = model

        now = datetime.now()
        self.now = TimeFormater.ensure_timezone(now)

        # convert other times
        self.model.created_at = TimeFormater.ensure_timezone(self.model.created_at)
        self.model.updated_at = TimeFormater.ensure_timezone(self.model.updated_at)
        self.model.data = json.dumps({"data": "stub"})

    def lock(self):
        """Receive a model and lock the time"""

        end_time = self.now + timedelta(minutes=10)
        self.model.automation_pause = True
        self.model.pause_init = self.now
        self.model.pause_end = end_time

        self.model.save()

    def unlock(self):
        self.model.automation_pause = False
        self.model.save()

    def is_locked(self):
        if self.model.automation_pause:
            return True
        else:
            return False


class TimeZoneChecker:  # TODO: remove static method
    @staticmethod
    def is_day(timezone='+00:00'):

        if timezone is None:
            timezone = '+00:00'

        now = datetime.now()
        init = datetime(year=now.year, month=now.month, day=now.day, hour=6)
        end = datetime(year=now.year, month=now.month, day=now.day, hour=21)

        init = TimeFormater.sum_timezone(init, timezone)
        end = TimeFormater.sum_timezone(end, timezone)

        init = init.time_delay
        end = end.time_delay
        if init <= now < end:
            return True
        else:
            return False


class TimeChecker:
    def is_day(self, timezone): # TODO
        """
        Return True if is day to the countries on received timezone
        :param timezone:
        :return: bool
        """
        pass

    @staticmethod
    def x_minutes_has_passed(first_time, step):
        now = datetime.now()
        delta = timedelta(minutes=step)

        if (now - first_time) >= delta:
            return True
        else:
            return False


class TimeZone:
    def __init__(self, time_str):
        self.time_str = time_str
        self.__convert()

    def __str__(self):
        return self.time_str

    def __len__(self):
        return len(self.time_str)

    def get(self):
        return self.time_str

    def __convert(self):
        if len(self.time_str) == 6:
            try:
                time = datetime.now()
                timezone = self.time_str.split(':')
                self.hour = int(timezone[0][1:])
                self.minutes = int(timezone[1])
                self.signal = timezone[0][0]
            except Exception as e:
                raise e
        else:
            raise ValueError('invalid format "{}" value must be like: +00:00'.format(self.time_str))
    @property
    def time_delay(self):
        delta = timedelta(hours=self.hour, minutes=self.minutes)
        time_delay = delta
        return time_delay

    def delay_to_midnight(self):
        now = datetime.now()
        midnight = now.replace(hour=23, minute=59, second=59)
        time_to = midnight - now
        if self.signal == '+':
            time_to = time_to - self.time_delay
        elif self.signal == '-':
            time_to = time_to + self.time_delay
        return time_to

