# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-09 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joan', '0041_auto_20170909_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='feature_text',
            field=models.CharField(max_length=200, unique=True, verbose_name='Feature Name'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='requirement_text',
            field=models.CharField(max_length=300, unique=True, verbose_name='Requirement Name'),
        ),
    ]