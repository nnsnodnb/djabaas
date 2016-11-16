# coding=utf-8

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from push.models import DeviceTokenModel, NotificationModel
from datetime import datetime
import os, os.path, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '../../modules/')
import push_notification

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        now = '{0:%Y/%m/%d %H:%M}'.format(datetime.now())
        notifications = NotificationModel.objects.filter(execute_datetime = now,
                                                         is_sent = False,
                                                         status = 0)

        for notification in notifications:
            device_tokens = DeviceTokenModel.objects.filter(os_version__gte = notification.os_version,
                                                            username = notification.username)
            self.prepare_push_notification(notification, device_tokens)

    def prepare_push_notification(self, notification, device_tokens):
        device_token_lists = []
        for item in device_tokens:
            device_token_lists.append(item.device_token)

        push_notification.execute(device_token_lists, notification)
