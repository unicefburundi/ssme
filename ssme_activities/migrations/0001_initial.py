# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Beneficiaire",
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
                ("designation", models.CharField(max_length=100)),
                ("nombre_mois_min", models.IntegerField(null=True, blank=True)),
                ("nombre_mois_max", models.IntegerField(null=True, blank=True)),
            ],
            options={"ordering": ("designation",)},
        ),
        migrations.CreateModel(
            name="Campaign",
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
                ("name", models.CharField(max_length=500)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("going_on", models.BooleanField(default=False)),
            ],
            options={"ordering": ("end_date",)},
        ),
        migrations.CreateModel(
            name="CampaignBeneficiary",
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
                ("order_in_sms", models.IntegerField()),
                ("beneficiary", models.ForeignKey(to="ssme_activities.Beneficiaire")),
                ("campaign", models.ForeignKey(to="ssme_activities.Campaign")),
            ],
            options={"ordering": ("beneficiary",)},
        ),
        migrations.CreateModel(
            name="CampaignBeneficiaryCDS",
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
                ("population_attendu", models.IntegerField(null=True)),
                ("population_obtenue", models.IntegerField(null=True)),
                ("campaign", models.ForeignKey(to="ssme_activities.Campaign")),
            ],
        ),
        migrations.CreateModel(
            name="CampaignBeneficiaryProduct",
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
                ("dosage", models.FloatField(null=True)),
                (
                    "campaign_beneficiary",
                    models.ForeignKey(to="ssme_activities.CampaignBeneficiary"),
                ),
            ],
            options={"ordering": ("campaign_beneficiary",)},
        ),
        migrations.CreateModel(
            name="CampaignCDS",
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
                ("population_cible", models.IntegerField(null=True)),
                ("enfant_moins_5_ans", models.IntegerField(null=True)),
                ("campaign", models.ForeignKey(to="ssme_activities.Campaign")),
            ],
        ),
        migrations.CreateModel(
            name="CampaignProduct",
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
                ("order_in_sms", models.IntegerField()),
                ("campaign", models.ForeignKey(to="ssme_activities.Campaign")),
            ],
            options={"ordering": ("product",)},
        ),
        migrations.CreateModel(
            name="CDS",
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
                ("name", models.CharField(max_length=40)),
                ("code", models.CharField(unique=True, max_length=6)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="District",
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
                ("name", models.CharField(unique=True, max_length=40)),
                ("code", models.IntegerField(unique=True)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=100)),
                ("can_be_fractioned", models.BooleanField(default=False)),
                ("unite_de_mesure", models.CharField(max_length=10)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="ProfileUser",
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
                (
                    "telephone",
                    models.CharField(
                        blank=True,
                        help_text="The telephone to contact you.",
                        max_length=16,
                        validators=[
                            django.core.validators.RegexValidator(
                                regex=b"^\\+?1?\\d{9,15}$",
                                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                            )
                        ],
                    ),
                ),
                (
                    "level",
                    models.CharField(
                        blank=True,
                        help_text="Either CDS, BDS, PBS, or Central level.",
                        max_length=3,
                        choices=[
                            (b"CEN", b"Central"),
                            (b"BPS", b"BPS"),
                            (b"BDS", b"BDS"),
                            (b"CDS", b"CDS"),
                        ],
                    ),
                ),
                (
                    "moh_facility",
                    models.CharField(
                        help_text="Code of the MoH facility",
                        max_length=8,
                        null=True,
                        blank=True,
                    ),
                ),
                ("user", models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("user",)},
        ),
        migrations.CreateModel(
            name="Province",
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
                ("name", models.CharField(unique=True, max_length=20)),
                ("code", models.IntegerField(unique=True)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="Report",
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
                ("reporting_date", models.DateField()),
                ("concerned_date", models.DateField()),
                ("text", models.CharField(max_length=200)),
                ("category", models.CharField(max_length=50)),
                ("cds", models.ForeignKey(to="ssme_activities.CDS")),
            ],
            options={"ordering": ("reporting_date",)},
        ),
        migrations.CreateModel(
            name="ReportBeneficiary",
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
                ("reception_date", models.DateField()),
                ("received_number", models.IntegerField()),
                (
                    "campaign_beneficiary",
                    models.ForeignKey(to="ssme_activities.CampaignBeneficiary"),
                ),
                ("report", models.ForeignKey(to="ssme_activities.Report")),
            ],
            options={"get_latest_by": "id"},
        ),
        migrations.CreateModel(
            name="Reporter",
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
                ("phone_number", models.CharField(max_length=20)),
                ("supervisor_phone_number", models.CharField(max_length=20)),
                ("cds", models.ForeignKey(to="ssme_activities.CDS")),
            ],
            options={"ordering": ("phone_number",)},
        ),
        migrations.CreateModel(
            name="ReportProductReception",
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
                ("reception_date", models.DateField()),
                ("received_quantity", models.FloatField()),
                (
                    "campaign_product",
                    models.ForeignKey(to="ssme_activities.CampaignProduct"),
                ),
                ("report", models.ForeignKey(to="ssme_activities.Report")),
            ],
            options={"get_latest_by": "id"},
        ),
        migrations.CreateModel(
            name="ReportProductRemainStock",
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
                ("concerned_date", models.DateField()),
                ("remain_quantity", models.FloatField()),
                (
                    "campaign_product",
                    models.ForeignKey(to="ssme_activities.CampaignProduct"),
                ),
                ("report", models.ForeignKey(to="ssme_activities.Report")),
            ],
            options={"get_latest_by": "id"},
        ),
        migrations.CreateModel(
            name="ReportStockOut",
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
                ("remaining_stock", models.FloatField()),
                (
                    "campaign_product",
                    models.ForeignKey(to="ssme_activities.CampaignProduct"),
                ),
                ("report", models.ForeignKey(to="ssme_activities.Report")),
            ],
        ),
        migrations.CreateModel(
            name="Temporary",
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
                ("phone_number", models.CharField(max_length=20)),
                ("supervisor_phone_number", models.CharField(max_length=20)),
                ("cds", models.ForeignKey(to="ssme_activities.CDS")),
            ],
        ),
        migrations.AddField(
            model_name="district",
            name="province",
            field=models.ForeignKey(to="ssme_activities.Province"),
        ),
        migrations.AddField(
            model_name="cds",
            name="district",
            field=models.ForeignKey(to="ssme_activities.District"),
        ),
        migrations.AddField(
            model_name="campaignproduct",
            name="product",
            field=models.ForeignKey(to="ssme_activities.Product"),
        ),
        migrations.AddField(
            model_name="campaigncds",
            name="cds",
            field=models.ForeignKey(to="ssme_activities.CDS"),
        ),
        migrations.AddField(
            model_name="campaignbeneficiaryproduct",
            name="campaign_product",
            field=models.ForeignKey(to="ssme_activities.CampaignProduct"),
        ),
        migrations.AddField(
            model_name="campaignbeneficiarycds",
            name="cds",
            field=models.ForeignKey(to="ssme_activities.CDS"),
        ),
        migrations.AlterUniqueTogether(
            name="campaignproduct", unique_together=set([("campaign", "order_in_sms")])
        ),
        migrations.AlterUniqueTogether(
            name="campaignbeneficiary",
            unique_together=set([("campaign", "order_in_sms")]),
        ),
    ]
