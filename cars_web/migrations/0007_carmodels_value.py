# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-16 07:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars_web', '0006_auto_20180126_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='carmodels',
            name='value',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]