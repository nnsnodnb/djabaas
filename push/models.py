from __future__ import unicode_literals

from datetime import datetime
from django.db import models

class DeviceTokenModel(models.Model):
    os_version = models.FloatField()
    device_token = models.CharField(max_length = 100, default = None)
    register_datetime = models.DateTimeField(default = datetime.now)
    update_datetime = models.DateTimeField(default = datetime.now)
    username = models.CharField(max_length = 50)

class NotificationModel(models.Model):
    title = models.CharField(max_length = 200, default = None)
    message = models.CharField(max_length = 500, default = None)
    os_version = models.FloatField()
    sound = models.CharField(max_length = 30, default = None)
    badge = models.IntegerField(default = None)
    url = models.CharField(max_length = 200, default = None)
    json = models.CharField(max_length = 150, default = None)
    content_available = models.BooleanField(default = False)
    is_production = models.BooleanField(default = False)
    register_date = models.DateTimeField(default = datetime.now)
    username = models.CharField(max_length = 50)

class DevelopFileModel(models.Model):
    upload_username = models.CharField(max_length = 50, default = None)
    development_file_name = models.CharField(max_length = 100, default = None)

class ProductFileModel(models.Model):
    upload_username = models.CharField(max_length = 50, default = None)
    production_file_name = models.CharField(max_length = 100, default = None)
