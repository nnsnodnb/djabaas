from __future__ import unicode_literals

from datetime import datetime
from django.db import models

class DeviceTokenModel(models.Model):
    os_version = models.CharField(max_length = 10)
    device_token = models.CharField(max_length = 100)
    register_datetime = models.DateTimeField(default = datetime.now)
    update_datetime = models.DateTimeField(default = datetime.now)
