# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-03 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0003_notificationmodel_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developfilemodel',
            name='development_file_name',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='developfilemodel',
            name='upload_username',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='devicetokenmodel',
            name='device_token',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='notificationmodel',
            name='badge',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='notificationmodel',
            name='json',
            field=models.CharField(default=None, max_length=150),
        ),
        migrations.AlterField(
            model_name='notificationmodel',
            name='message',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='notificationmodel',
            name='sound',
            field=models.CharField(default=None, max_length=30),
        ),
        migrations.AlterField(
            model_name='notificationmodel',
            name='title',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='notificationmodel',
            name='url',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='productfilemodel',
            name='production_file_name',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='productfilemodel',
            name='upload_username',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
