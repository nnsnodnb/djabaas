# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-09-25 08:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('message', models.CharField(max_length=500)),
                ('os_version', models.CharField(max_length=10)),
                ('sound', models.CharField(max_length=30)),
                ('badge', models.IntegerField()),
                ('url', models.CharField(max_length=200)),
                ('json', models.CharField(max_length=150)),
                ('content_available', models.BooleanField(default=False)),
                ('is_production', models.BooleanField(default=False)),
            ],
        ),
    ]
