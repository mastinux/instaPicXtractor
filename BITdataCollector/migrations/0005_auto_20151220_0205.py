# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BITdataCollector', '0004_auto_20151220_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='facebook_page_url',
            field=models.CharField(max_length=511, null=True),
        ),
    ]
