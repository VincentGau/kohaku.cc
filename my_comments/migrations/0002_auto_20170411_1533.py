# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-04-11 07:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_comments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentwithtitle',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='commentwithtitle',
            name='site',
        ),
        migrations.RemoveField(
            model_name='commentwithtitle',
            name='user',
        ),
        migrations.DeleteModel(
            name='CommentWithTitle',
        ),
    ]