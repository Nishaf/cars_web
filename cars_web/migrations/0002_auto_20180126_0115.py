# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars_web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarModelsInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('website', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('make', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameModel(
            old_name='CarsInfo',
            new_name='CarsDetails',
        ),
    ]
