# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssme_activities', '0003_auto_20151117_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='reporting_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
