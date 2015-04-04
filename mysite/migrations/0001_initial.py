# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wallpaper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'Untitled', max_length=250)),
                ('author', models.CharField(max_length=150, null=True, blank=True)),
                ('url', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
