# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-04 09:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_auto_20150417_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallpaper',
            name='image',
            field=models.ImageField(upload_to='wallpapers'),
        ),
        migrations.AlterField(
            model_name='wallpaper',
            name='title',
            field=models.CharField(default='Untitled', max_length=250),
        ),
    ]