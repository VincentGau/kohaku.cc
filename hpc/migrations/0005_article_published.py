# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-04-11 07:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0004_auto_20170308_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
