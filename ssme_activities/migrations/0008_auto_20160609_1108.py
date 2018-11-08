# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("ssme_activities", "0007_auto_20151118_1138")]

    operations = [
        migrations.CreateModel(
            name="AllSupervisorsOnDistrictLevel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("phone_number", models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name="DistrictSupervisor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("district", models.ForeignKey(to="ssme_activities.District")),
                (
                    "supervisor",
                    models.ForeignKey(
                        to="ssme_activities.AllSupervisorsOnDistrictLevel"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="campaignbeneficiaryproduct",
            name="order_in_sms",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="reportbeneficiary",
            name="beneficiaries_per_product",
            field=models.ForeignKey(
                default=1, to="ssme_activities.CampaignBeneficiaryProduct"
            ),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name="campaignbeneficiary",
            unique_together=set([("campaign", "beneficiary")]),
        ),
        migrations.AlterUniqueTogether(
            name="campaignbeneficiaryproduct",
            unique_together=set(
                [("campaign_beneficiary", "campaign_product", "order_in_sms")]
            ),
        ),
        migrations.AlterUniqueTogether(
            name="campaignproduct",
            unique_together=set([("campaign", "product", "order_in_sms")]),
        ),
    ]
