# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('BITdataCollector', '0005_auto_20151220_0205'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='place',
            field=models.CharField(default=datetime.datetime(2016, 7, 7, 16, 49, 44, 826075, tzinfo=utc), max_length=255),
            preserve_default=False,
        ),
    ]
