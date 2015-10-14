# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssme_activities', '0002_auto_20151012_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaignbeneficiarycds',
            name='campaign_beneficiary',
        ),
        migrations.AddField(
            model_name='campaignbeneficiarycds',
            name='campaign',
            field=models.ForeignKey(default=1, to='ssme_activities.Campaign'),
            preserve_default=False,
        ),
    ]
