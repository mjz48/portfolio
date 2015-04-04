# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallpaper',
            name='url',
            field=models.ImageField(upload_to=b''),
            preserve_default=True,
        ),
    ]
