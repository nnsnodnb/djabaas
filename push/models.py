from __future__ import unicode_literals

from datetime import datetime
from django.db import models

class DeviceTokenModel(models.Model):
    os_version = models.CharField(max_length = 10)
    device_token = models.CharField(max_length = 100)
    register_datetime = models.DateTimeField(default = datetime.now)
    update_datetime = models.DateTimeField(default = datetime.now)

class NotificationModel(models.Model):
    title = models.CharField(max_length = 200)
    message = models.CharField(max_length = 500)
    os_version = models.CharField(max_length = 10)
    sound = models.CharField(max_length = 30)
    badge = models.IntegerField()
    url = models.CharField(max_length = 200)
    json = models.CharField(max_length = 150)
    content_available = models.BooleanField(default = False)
    is_production = models.BooleanField(default = False)
    register_date = models.DateTimeField(default = datetime.now)
