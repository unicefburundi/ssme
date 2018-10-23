# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("ssme_activities", "0005_auto_20151118_1135")]

    operations = [
        migrations.AlterField(
            model_name="reportbeneficiary",
            name="report",
            field=models.ForeignKey(to="ssme_activities.Report", null=True),
        )
    ]
