# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficiaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('designation', models.CharField(max_length=100)),
                ('priority', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('open', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CampaignBeneficiary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_in_sms', models.IntegerField()),
                ('beneficairy', models.ForeignKey(to='ssme_activities.Beneficiaire')),
                ('campaign', models.ForeignKey(to='ssme_activities.Campaign')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignBeneficiaryProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dosage', models.FloatField()),
                ('camapaign_beneficiary', models.ForeignKey(to='ssme_activities.CampaignBeneficiary')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignCDS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('campaign', models.ForeignKey(to='ssme_activities.Campaign')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignCDSBeneficiary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expected_number', models.IntegerField()),
                ('beneficiary', models.ForeignKey(to='ssme_activities.CampaignBeneficiary')),
                ('campaign_cds', models.ForeignKey(to='ssme_activities.CampaignCDS')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignCDSProduit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('campaign_cds', models.ForeignKey(to='ssme_activities.CampaignCDS')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_in_sms', models.IntegerField()),
                ('campaign', models.ForeignKey(to='ssme_activities.Campaign')),
            ],
        ),
        migrations.CreateModel(
            name='CDS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('code', models.CharField(unique=True, max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('code', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.IntegerField()),
                ('can_be_fractioned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('code', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateField()),
                ('text', models.CharField(max_length=200)),
                ('cds', models.ForeignKey(to='ssme_activities.CDS')),
            ],
        ),
        migrations.CreateModel(
            name='ReportBeneficiary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reception_date', models.DateField()),
                ('received_number', models.IntegerField()),
                ('campaign_cds_beneficiary', models.ForeignKey(to='ssme_activities.CampaignCDSBeneficiary')),
            ],
        ),
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('supervisor_phone_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ReportProductReception',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reception_date', models.DateField()),
                ('received_quantity', models.IntegerField()),
                ('campaign_cds_product', models.ForeignKey(to='ssme_activities.CampaignCDSProduit')),
            ],
        ),
        migrations.CreateModel(
            name='ReportProductStock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('concerned_date', models.DateField()),
                ('remain_quantity', models.IntegerField()),
                ('campaign_cds_product', models.ForeignKey(to='ssme_activities.CampaignCDSProduit')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=40)),
                ('prenom', models.CharField(max_length=40)),
                ('login', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=40)),
                ('level', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='district',
            name='province',
            field=models.ForeignKey(to='ssme_activities.Province'),
        ),
        migrations.AddField(
            model_name='cds',
            name='district',
            field=models.ForeignKey(to='ssme_activities.District'),
        ),
        migrations.AddField(
            model_name='campaignproduct',
            name='product',
            field=models.ForeignKey(to='ssme_activities.Product'),
        ),
        migrations.AddField(
            model_name='campaigncdsproduit',
            name='produit',
            field=models.ForeignKey(to='ssme_activities.Product'),
        ),
        migrations.AddField(
            model_name='campaigncds',
            name='cds',
            field=models.ForeignKey(to='ssme_activities.CDS'),
        ),
        migrations.AddField(
            model_name='campaignbeneficiaryproduct',
            name='campaign_product',
            field=models.ForeignKey(to='ssme_activities.CampaignProduct'),
        ),
        migrations.AlterUniqueTogether(
            name='campaignproduct',
            unique_together=set([('campaign', 'product', 'order_in_sms')]),
        ),
        migrations.AlterUniqueTogether(
            name='campaignbeneficiary',
            unique_together=set([('campaign', 'beneficairy', 'order_in_sms')]),
        ),
    ]
