# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssme_activities', '0004_auto_20151117_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportbeneficiary',
            name='received_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='reportproductreception',
            name='received_quantity',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='reportproductremainstock',
            name='remain_quantity',
            field=models.FloatField(null=True),
        ),
    ]
