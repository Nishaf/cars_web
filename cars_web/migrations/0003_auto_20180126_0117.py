# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars_web', '0002_auto_20180126_0115'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CarModelsInfo',
            new_name='CarModels',
        ),
    ]
