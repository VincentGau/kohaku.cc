# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-03-08 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0002_auto_20170302_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='type',
            field=models.CharField(default='life', max_length=20),
        ),
    ]