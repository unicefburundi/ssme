# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssme_activities', '0003_auto_20151006_0912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='open',
            new_name='going_on',
        ),
    ]
