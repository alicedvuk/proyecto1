# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Girl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Incall Girl'), (2, 'Outcall Girl'), (3, 'Ex Girl')], db_index=True, default=1, verbose_name='Status')),
                ('name', models.CharField(max_length=50, null=True, verbose_name='Name Girl')),
                ('phone', models.CharField(max_length=20, null=True, verbose_name='Phone number')),
                ('mobile_phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Mobile Phone number')),
                ('postcode', models.CharField(max_length=50, null=True, verbose_name='Postcode')),
                ('address', models.CharField(max_length=50, null=True, verbose_name='Adress')),
                ('flat', models.CharField(blank=True, max_length=20, null=True, verbose_name='Flat')),
                ('tube_station', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tube Station ')),
                ('email', models.CharField(blank=True, max_length=50, null=True, verbose_name='Email')),
                ('live_with', models.CharField(blank=True, max_length=90, null=True, verbose_name='Live With')),
                ('date', models.DateTimeField(verbose_name='Date started working')),
            ],
        ),
    ]
