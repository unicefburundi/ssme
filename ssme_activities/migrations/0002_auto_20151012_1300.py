# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssme_activities', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaigncdsbeneficiaries',
            name='beneficiaires',
        ),
        migrations.RemoveField(
            model_name='campaigncdsbeneficiaries',
            name='cds',
        ),
        migrations.DeleteModel(
            name='CampaignCDSBeneficiaries',
        ),
    ]
