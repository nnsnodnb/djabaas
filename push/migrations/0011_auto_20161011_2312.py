# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-11 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0010_auto_20161009_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationmodel',
            name='execute_datetime',
            field=models.CharField(default='2016/10/11 23:12', max_length=16),
        ),
    ]
