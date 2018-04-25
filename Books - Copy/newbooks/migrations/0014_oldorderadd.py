# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-21 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newbooks', '0013_auto_20170720_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='oldorderadd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(max_length=300)),
                ('pincode', models.IntegerField()),
                ('state', models.CharField(default='Delhi', max_length=25)),
                ('mob', models.IntegerField()),
                ('datecreate', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
