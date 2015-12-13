# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BITdataCollector', '0004_auto_20151213_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='country',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='city',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='City',
        ),
    ]
