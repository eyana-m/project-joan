# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 07:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('joan', '0030_auto_20170903_0609'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feature',
            old_name='requirement',
            new_name='requirements',
        ),
    ]