# work_calendar.py
import pandas as pd
import pytz
from workalendar.europe import Russia

class WorkCalendar:
    def __init__(self, timezone='Europe/Moscow'):
        self.timezone = timezone
        self.moscow_tz = pytz.timezone(timezone)
        self.cal = Russia()

    def is_working_day(self, date):
        return self.cal.is_working_day(date)

    def get_working_hours(self, date, work_start='09:00:00', work_end='18:00:00'):
        """Возвращает временные границы рабочего дня."""
        work_start_time = pd.Timestamp.combine(date.date(), pd.Timestamp(work_start).time()).tz_localize(self.timezone)
        work_end_time = pd.Timestamp.combine(date.date(), pd.Timestamp(work_end).time()).tz_localize(self.timezone)
        return work_start_time, work_end_time