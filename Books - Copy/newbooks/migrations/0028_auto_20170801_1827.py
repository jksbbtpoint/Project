# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-01 12:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newbooks', '0027_auto_20170801_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='likesonpost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.IntegerField()),
                ('bg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newbooks.blog')),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='likes',
        ),
    ]
