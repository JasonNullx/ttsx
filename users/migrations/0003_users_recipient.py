# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170531_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='recipient',
            field=models.CharField(max_length=40, blank=True),
        ),
    ]
