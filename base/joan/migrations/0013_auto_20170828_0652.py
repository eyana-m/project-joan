# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 06:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('joan', '0012_release'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='iteration',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='release',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='joan.Release'),
        ),
    ]
