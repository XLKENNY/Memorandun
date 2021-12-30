# linux
# Celery
# config.py
# author:KENNY

from datetime import timedelta
from celery.schedules import crontab

CELERY_TIMEZONE = "Asia/Shanghai"
CELERYBEAT_SCHEDULE = { 
    "every-7s-check-alarm-time": {
        "task": "memorandum_alarm.worker",
        "schedule":timedelta(seconds=7),
        "args":("alarm",)
    }   
}

"""
    this is feature_2 modify
"""