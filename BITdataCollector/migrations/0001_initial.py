# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('facebook_page_ulr', models.CharField(max_length=511)),
                ('upcoming_event_count', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=255)),
                ('tracker_count', models.IntegerField(default=0)),
                ('mbid', models.CharField(max_length=255)),
                ('image_url', models.CharField(max_length=511)),
                ('facebook_tour_dates_url', models.CharField(max_length=511)),
                ('thumb_url', models.CharField(max_length=511)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1023)),
                ('title', models.CharField(max_length=511)),
                ('ticket_type', models.CharField(max_length=255)),
                ('facebook_rsvp_url', models.CharField(max_length=511)),
                ('ticket_url', models.CharField(max_length=511)),
                ('formatted_datetime', models.CharField(max_length=255)),
                ('formatted_location', models.CharField(max_length=255)),
                ('ticket_status', models.CharField(max_length=255)),
                ('artists', models.ManyToManyField(to='BITdataCollector.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(to='BITdataCollector.Venue'),
        ),
    ]
