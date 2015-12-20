# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BITdataCollector', '0002_auto_20151220_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='facebook_tour_dates_url',
            field=models.CharField(max_length=511, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='BIT_event_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='on_sale_datetime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='venue',
            name='region',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
