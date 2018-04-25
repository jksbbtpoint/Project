# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-13 11:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newbooks', '0042_auto_20170810_2053'),
    ]

    operations = [
        migrations.CreateModel(
            name='donate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=80)),
                ('ContactNo', models.IntegerField(max_length=10)),
                ('pic1', models.FileField(blank=True, null=True, upload_to='pic')),
                ('pic2', models.FileField(blank=True, null=True, upload_to='pic')),
                ('YourPrice', models.IntegerField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='returnbook',
            unique_together=set([('orderno', 'isbn')]),
        ),
    ]
