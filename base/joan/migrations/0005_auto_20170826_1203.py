# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-26 12:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('joan', '0004_auto_20170826_1158'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='requirement',
            options={'ordering': ['reqd_id', 'id']},
        ),
    ]
