# coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from push.models import DeviceTokenModel, NotificationModel
from datetime import datetime

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        now = '{0:%Y/%m/%d %H:%M}'.format(datetime.now())
        notification = NotificationModel.objects.filter(execute_datetime = now)
