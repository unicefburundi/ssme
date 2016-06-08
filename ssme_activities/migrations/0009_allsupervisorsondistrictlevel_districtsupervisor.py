# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssme_activities', '0008_auto_20160411_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllSupervisorsOnDistrictLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='DistrictSupervisor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('district', models.ForeignKey(to='ssme_activities.District')),
                ('supervisor', models.ForeignKey(to='ssme_activities.AllSupervisorsOnDistrictLevel')),
            ],
        ),
    ]
