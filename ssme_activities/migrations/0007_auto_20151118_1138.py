# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("ssme_activities", "0006_auto_20151118_1137")]

    operations = [
        migrations.AlterField(
            model_name="reportproductreception",
            name="report",
            field=models.ForeignKey(to="ssme_activities.Report", null=True),
        ),
        migrations.AlterField(
            model_name="reportproductremainstock",
            name="report",
            field=models.ForeignKey(to="ssme_activities.Report", null=True),
        ),
    ]
