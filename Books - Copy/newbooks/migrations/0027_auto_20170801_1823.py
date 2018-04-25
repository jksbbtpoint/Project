# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-01 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newbooks', '0026_preimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='Category',
            field=models.CharField(blank=True, choices=[('Academics', 'Academics'), ('Network Marketing', 'Network Marketing'), ('Self Help', 'Self Help'), ('Leadership', 'Leadership'), ('Ebook', 'Ebook')], default='Self Help', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='desc',
            field=models.TextField(blank=True, max_length=20000),
        ),
    ]
