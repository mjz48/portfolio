# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_auto_20150406_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallpaper',
            name='link',
            field=models.URLField(max_length=1000),
            preserve_default=True,
        ),
    ]
