# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars_web', '0004_delete_carsdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarsDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('website', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('make', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=500)),
                ('link', models.CharField(max_length=500)),
            ],
        ),
    ]
