# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BITdataCollector', '0003_auto_20151213_0021'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='venue',
            name='country',
        ),
        migrations.AlterField(
            model_name='venue',
            name='city',
            field=models.ForeignKey(to='BITdataCollector.City'),
        ),
    ]
