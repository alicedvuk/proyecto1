# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-09 23:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escort_profile', '0005_auto_20160709_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='escort',
            name='photo_3',
            field=models.ImageField(blank=True, null=True, upload_to='london-escort-agency/%Y/%m/%d', verbose_name='Pic 4'),
        ),
        migrations.AddField(
            model_name='escort',
            name='photo_4',
            field=models.ImageField(blank=True, null=True, upload_to='london-escort-agency/%Y/%m/%d', verbose_name='Pic 4'),
        ),
        migrations.AlterField(
            model_name='escort',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='london-escort-agency/%Y/%m/%d', verbose_name='Pic 1'),
        ),
        migrations.AlterField(
            model_name='escort',
            name='photo_1',
            field=models.ImageField(blank=True, null=True, upload_to='london-escort-agency/%Y/%m/%d', verbose_name='Pic 2'),
        ),
        migrations.AlterField(
            model_name='escort',
            name='photo_2',
            field=models.ImageField(blank=True, null=True, upload_to='london-escort-agency/%Y/%m/%d', verbose_name='Pic 3'),
        ),
    ]
