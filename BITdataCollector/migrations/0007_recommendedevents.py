# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BITdataCollector', '0006_venue_place'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendedEvents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('radius', models.FloatField(default=0)),
                ('event', models.ForeignKey(related_name='main_event', to='BITdataCollector.Event')),
                ('events', models.ManyToManyField(related_name='recommended_events', to='BITdataCollector.Event')),
            ],
        ),
    ]
