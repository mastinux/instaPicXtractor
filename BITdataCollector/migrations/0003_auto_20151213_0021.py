# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BITdataCollector', '0002_auto_20151212_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='mbid',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
