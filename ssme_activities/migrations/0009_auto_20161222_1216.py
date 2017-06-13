# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssme_activities', '0008_auto_20160609_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignbeneficiary',
            name='pourcentage_attendu',
            field=models.FloatField(default=100.0, null=True),
        ),
    ]
