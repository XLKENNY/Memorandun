# -*- coding:utf-8 -*-
# memorandum
# time_converter.py
# author: kenny

import sys
import time
import re
from datetime import datetime
from datetime import timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *
from . import log_ctrl


class ChangeTime():
    def __init__(self, date1):
        self.dt = date1

    def time_change_cn(self):
        """Convert all the Chinese in dt into English format"""
        self.dt = self.dt.replace('年', '/').replace('月', '/').replace('日 ', ' /').replace('.', '/').replace('时', '/').replace('分', '/').replace('秒', '/').replace('点', '/')

    def time_add(self):
        """
        Dt is already a formatted date
        If the time is incomplete, it will be automatically added to the time of the next day
        """
        default_time = datetime.now() + timedelta(days=1)
        # First save the next day's time, if the corresponding time position incoming data, then replace with the incoming time
        dt_date = {
            'dt_year': default_time.year,
            'dt_month': default_time.month,
            'dt_day': default_time.day,
            'dt_hour': default_time.hour,
            'dt_minute': default_time.minute,
            'dt_second': default_time.second
        }
        # Used for regular matching of time data, the parameter order defaults to year, month, day, hour, minute and second
        re_date = ['\d{4}', '\d?\d']  
        self.dt = re.compile('[/: ]').split(self.dt)  
        for t in dt_date:  # Start searching, matching and replacing
            if(self.dt):
                if (re.search(re_date[0], self.dt[0])):
                    dt_date[t] = self.dt[0]
                    del self.dt[0]
                if (re_date[0] == '\d{4}'):  # When a time position matches, the removal is no longer matched
                    del re_date[0]
        self.dt = default_time.replace(
                            year=int(dt_date['dt_year']),
                            month=int(dt_date['dt_month']),
                            day=int(dt_date['dt_day']),
                            hour=int(dt_date['dt_hour']),
                            minute=int(dt_date['dt_minute']),
                            second=int(dt_date['dt_second'])
                            )

    def time_change_f(self):
        """
        Dt is the final number. Converts dt to the specified format
        """
        fmt = "%Y-%m-%d %X"
        data1 = parser.parse(str(self.dt))
        self.dt = str(data1.strftime(fmt))
