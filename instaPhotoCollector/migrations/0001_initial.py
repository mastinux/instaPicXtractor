# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instagram_id', models.IntegerField()),
                ('std_resolution_url', models.CharField(max_length=512)),
                ('low_resolution_url', models.CharField(max_length=512)),
                ('thumbnail_url', models.CharField(max_length=512)),
                ('location', models.CharField(max_length=1024)),
                ('longitude', models.FloatField(default=0)),
                ('latitude', models.FloatField(default=0)),
                ('created_time', models.DateTimeField()),
                ('like_count', models.IntegerField(default=0)),
                ('event', models.IntegerField()),
            ],
        ),
    ]
