# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('BITdataCollector', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artist',
            old_name='facebook_page_ulr',
            new_name='facebook_page_url',
        ),
        migrations.AddField(
            model_name='event',
            name='BIT_event_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 20, 1, 3, 36, 218649, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='on_sale_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 20, 1, 2, 55, 175600, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='venue',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='venue',
            name='longitude',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='venue',
            name='region',
            field=models.CharField(default=2, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='artist',
            name='mbid',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(max_length=1023, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='ticket_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='ticket_url',
            field=models.CharField(max_length=511, null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='country',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
