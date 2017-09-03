# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joan', '0033_auto_20170903_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='feature_status',
            field=models.CharField(choices=[(1, 'New'), (2, 'Use Case Done'), (3, 'In Progress'), (4, 'Done')], default=1, max_length=2),
        ),
    ]
