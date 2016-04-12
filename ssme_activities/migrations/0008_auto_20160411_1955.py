# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssme_activities', '0007_auto_20151118_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignbeneficiaryproduct',
            name='order_in_sms',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reportbeneficiary',
            name='beneficiaries_per_product',
            field=models.ForeignKey(default=0, to='ssme_activities.CampaignBeneficiaryProduct'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='campaignbeneficiary',
            unique_together=set([('campaign', 'beneficiary')]),
        ),
        migrations.AlterUniqueTogether(
            name='campaignbeneficiaryproduct',
            unique_together=set([('campaign_beneficiary', 'campaign_product', 'order_in_sms')]),
        ),
        migrations.AlterUniqueTogether(
            name='campaignproduct',
            unique_together=set([('campaign', 'product', 'order_in_sms')]),
        ),
    ]
