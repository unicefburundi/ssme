# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ssme_activities', '0002_auto_20151104_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cds',
            name='district',
            field=models.ForeignKey(verbose_name=b'district', to='ssme_activities.District'),
        ),
        migrations.AlterField(
            model_name='cds',
            name='name',
            field=models.CharField(max_length=40, verbose_name=b'nom'),
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(unique=True, max_length=40, verbose_name=b'nom'),
        ),
        migrations.AlterField(
            model_name='district',
            name='province',
            field=models.ForeignKey(verbose_name=b'province', to='ssme_activities.Province'),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='level',
            field=models.CharField(blank=True, help_text='Either CDS, BDS, PBS, or Central level.', max_length=3, verbose_name=b'niveau', choices=[(b'CEN', b'Central'), (b'BPS', b'BPS'), (b'BDS', b'BDS'), (b'CDS', b'CDS')]),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='moh_facility',
            field=models.CharField(help_text='Code of the MoH facility', max_length=8, null=True, verbose_name=b'code', blank=True),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='telephone',
            field=models.CharField(blank=True, help_text='The telephone to contact you.', max_length=16, verbose_name=b't\xc3\xa9l\xc3\xa9phone', validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]),
        ),
        migrations.AlterField(
            model_name='province',
            name='name',
            field=models.CharField(unique=True, max_length=20, verbose_name=b'nom'),
        ),
    ]
