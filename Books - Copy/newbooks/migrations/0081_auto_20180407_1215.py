# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-07 06:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newbooks', '0080_profile_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='myid',
            field=models.IntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='profile',
            name='sponsorid',
            field=models.IntegerField(default='0'),
        ),
    ]
