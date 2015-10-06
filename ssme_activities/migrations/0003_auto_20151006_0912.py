# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssme_activities', '0002_temporary'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beneficiaire',
            options={'ordering': ('designation',)},
        ),
        migrations.AlterModelOptions(
            name='campaign',
            options={'ordering': ('end_date',)},
        ),
        migrations.AlterModelOptions(
            name='campaignbeneficiary',
            options={'ordering': ('beneficairy',)},
        ),
        migrations.AlterModelOptions(
            name='campaignbeneficiaryproduct',
            options={'ordering': ('campaign_beneficiary',)},
        ),
        migrations.AlterModelOptions(
            name='campaignproduct',
            options={'ordering': ('product',)},
        ),
        migrations.AlterModelOptions(
            name='cds',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='district',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='profileuser',
            options={'ordering': ('user',)},
        ),
        migrations.AlterModelOptions(
            name='province',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ('reporting_date',)},
        ),
        migrations.AlterModelOptions(
            name='reportbeneficiary',
            options={'ordering': ('reception_date',)},
        ),
        migrations.AlterModelOptions(
            name='reporter',
            options={'ordering': ('phone_number',)},
        ),
        migrations.AlterModelOptions(
            name='reportproductreception',
            options={'ordering': ('reception_date',)},
        ),
        migrations.AlterModelOptions(
            name='reportproductremainstock',
            options={'ordering': ('report',)},
        ),
        migrations.RenameField(
            model_name='campaignbeneficiaryproduct',
            old_name='camapaign_beneficiary',
            new_name='campaign_beneficiary',
        ),
    ]
