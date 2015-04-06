# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_auto_20150403_1824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallpaper',
            name='url',
        ),
        migrations.AddField(
            model_name='wallpaper',
            name='image',
            field=models.ImageField(default='http://www.google.com', upload_to=b'wallpapers'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wallpaper',
            name='link',
            field=models.URLField(default='http://www.google.com'),
            preserve_default=False,
        ),
    ]
