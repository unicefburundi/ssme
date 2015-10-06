# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssme_activities', '0002_temporary'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cds',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='district',
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
    ]
