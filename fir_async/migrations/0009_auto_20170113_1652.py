# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-13 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fir_async', '0008_auto_20161014_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationtemplate',
            name='event',
            field=models.CharField(max_length=60, verbose_name='event'),
        ),
    ]
