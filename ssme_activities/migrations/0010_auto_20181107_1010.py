# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssme_activities', '0009_auto_20161222_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignbeneficiaryproduct',
            name='dosage',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
