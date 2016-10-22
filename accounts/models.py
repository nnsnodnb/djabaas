# coding: utf-8

from __future__ import unicode_literals

from django.db import models

class UserActivateTokenModel(models.Model):
    username = models.CharField(max_length = 50)
    token = models.CharField(max_length = 100)
    is_user = models.BooleanField(default = False)
