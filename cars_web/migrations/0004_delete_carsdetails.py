# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars_web', '0003_auto_20180126_0117'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CarsDetails',
        ),
    ]
