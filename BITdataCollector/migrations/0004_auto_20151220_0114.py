# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BITdataCollector', '0003_auto_20151220_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='on_sale_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
