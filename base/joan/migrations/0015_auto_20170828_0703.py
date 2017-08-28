# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 07:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('joan', '0014_auto_20170828_0656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requirement',
            name='project',
        ),
        migrations.AddField(
            model_name='release',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='joan.Project'),
        ),
        migrations.AddField(
            model_name='requirement',
            name='release',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='joan.Release'),
        ),
    ]
