# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars_web', '0005_carsdetails'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carsdetails',
            old_name='name',
            new_name='title',
        ),
    ]
