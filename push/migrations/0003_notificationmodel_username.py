# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-03 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0002_devicetokenmodel_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationmodel',
            name='username',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]