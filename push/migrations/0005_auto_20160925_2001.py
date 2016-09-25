# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-09-25 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0004_pemfilemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='DevelopFileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('development_file_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProductFileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('production_file_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='PemfileModel',
        ),
    ]
