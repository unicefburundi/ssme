# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("ssme_activities", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="campaignbeneficiary",
            name="pourcentage_attendu",
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AddField(
            model_name="campaignbeneficiaryproduct",
            name="pourcentage_attendu",
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
