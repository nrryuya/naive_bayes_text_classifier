# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 01:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='title',
            field=models.CharField(default='SOME STRING', max_length=255, verbose_name='タイトル'),
        ),
    ]