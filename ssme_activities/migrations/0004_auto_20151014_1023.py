# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssme_activities', '0003_auto_20151014_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiaire',
            name='nombre_mois_max',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='beneficiaire',
            name='nombre_mois_min',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
