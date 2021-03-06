import django_tables2 as tables
from ssme_activities.models import *


class ReportBeneficiaryTable(tables.Table):
    cds = tables.Column(accessor="report.cds")
    district = tables.Column(accessor="report.cds.district")
    province = tables.Column(accessor="report.cds.district.province")

    class Meta:
        model = ReportBeneficiary
        attrs = {
            "class": "table ",
            "data-toggle": "table",
            "data-search": "true",
            "data-show-columns": "true",
            "data-show-export": "true",
            "data-export-types": "['csv','excel']",
        }
        exclude = ("id", "report")


class ReportProductReceptionTable(tables.Table):
    cds = tables.Column(accessor="report.cds")
    district = tables.Column(accessor="report.cds.district")
    province = tables.Column(accessor="report.cds.district.province")

    class Meta:
        model = ReportProductReception
        attrs = {
            "class": "table ",
            "data-toggle": "table",
            "data-search": "true",
            "data-show-columns": "true",
            "data-show-export": "true",
            "data-export-types": "['csv','excel']",
        }
        exclude = ("id", "report")


class ReportProductRemainStockTable(tables.Table):
    cds = tables.Column(accessor="report.cds")
    district = tables.Column(accessor="report.cds.district")
    province = tables.Column(accessor="report.cds.district.province")

    class Meta:
        model = ReportProductRemainStock
        attrs = {
            "class": "table ",
            "data-toggle": "table",
            "data-search": "true",
            "data-show-columns": "true",
            "data-show-export": "true",
            "data-export-types": "['csv','excel']",
        }
        exclude = ("id", "report")
