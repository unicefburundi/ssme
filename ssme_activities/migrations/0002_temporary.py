# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssme_activities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temporary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('supervisor_phone_number', models.CharField(max_length=20)),
                ('cds', models.ForeignKey(to='ssme_activities.CDS')),
            ],
        ),
    ]
