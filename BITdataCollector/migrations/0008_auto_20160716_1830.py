# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('BITdataCollector', '0007_recommendedevents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendedevents',
            name='radius',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(241)]),
        ),
    ]
