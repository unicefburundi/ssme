# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssme_activities', '0010_auto_20181107_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignbeneficiaryproduct',
            name='campaign_beneficiary',
            field=models.ForeignKey(related_name='campaign_beneficiary', to='ssme_activities.CampaignBeneficiary'),
        ),
        migrations.AlterField(
            model_name='campaignbeneficiaryproduct',
            name='campaign_product',
            field=models.ForeignKey(related_name='campaign_product', to='ssme_activities.CampaignProduct'),
        ),
    ]
