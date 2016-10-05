from __future__ import unicode_literals

from datetime import datetime
from django.db import models
from django.utils.timezone import now

class DeviceTokenModel(models.Model):
    os_version = models.FloatField()
    device_token = models.CharField(max_length = 100, blank = True)
    register_datetime = models.DateTimeField(default = datetime.now)
    update_datetime = models.DateTimeField(default = datetime.now)
    username = models.CharField(max_length = 50)

class NotificationModel(models.Model):
    title = models.CharField(max_length = 200, blank = True)
    message = models.CharField(max_length = 500, blank = True)
    os_version = models.FloatField()
    sound = models.CharField(max_length = 30, blank = True)
    badge = models.IntegerField(blank = True)
    url = models.CharField(max_length = 200, blank = True)
    json = models.CharField(max_length = 150, blank = True)
    content_available = models.BooleanField(default = False)
    is_production = models.BooleanField(default = False)
    register_date = models.DateTimeField(default = datetime.now)
    username = models.CharField(max_length = 50)
    execute_datetime = models.CharField(max_length = 16, default = '{0:%Y/%m/%d %H:%M}'.format(datetime.now()))

class DevelopFileModel(models.Model):
    upload_username = models.CharField(max_length = 50, blank = True)
    development_file_name = models.CharField(max_length = 100, blank = True)

class ProductFileModel(models.Model):
    upload_username = models.CharField(max_length = 50, blank = True)
    production_file_name = models.CharField(max_length = 100, blank = True)
