# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-01 05:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fingouser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
