# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 13:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('joan', '0016_project_project_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='project_slug',
            new_name='slug',
        ),
    ]
