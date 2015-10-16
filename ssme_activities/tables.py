import django_tables2 as tables
from ssme_activities.models import *
from django_tables2.utils import A # alias for Accessor
from django.utils.safestring import SafeString


class ReportBeneficiaryTable(tables.Table):
    cds = tables.Column(accessor='report.cds')
    district = tables.Column(accessor='report.cds.district')
    province = tables.Column(accessor='report.cds.district.province')

    class Meta:
        model = ReportBeneficiary
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" ,  "data-show-export":"true", 'data-export-types': "['csv','excel']"}
        exclude = ('id', 'report')

class ReportProductReceptionTable(tables.Table):
    cds = tables.Column(accessor='report.cds')
    district = tables.Column(accessor='report.cds.district')
    province = tables.Column(accessor='report.cds.district.province')

    class Meta:
        model = ReportProductReception
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" ,  "data-show-export":"true", 'data-export-types': "['csv','excel']"}
        exclude = ('id', 'report')

class ReportProductRemainStockTable(tables.Table):
    cds = tables.Column(accessor='report.cds')
    district = tables.Column(accessor='report.cds.district')
    province = tables.Column(accessor='report.cds.district.province')

    class Meta:
        model = ReportProductRemainStock
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" ,  "data-show-export":"true", 'data-export-types': "['csv','excel']"}
        exclude = ('id', 'report')

class ReportBeneficiaryTable2(tables.Table):
    _6_11mois = tables.Column(verbose_name="6_11mois")
    _12_23_mois = tables.Column(verbose_name="12_23_mois")
    _24_59_mois = tables.Column(verbose_name="24_59_mois")
    _5_14_ans = tables.Column(verbose_name="5_14_ans")
    femmes_anceintes = tables.Column(verbose_name="femmes_anceintes")

    class Meta:
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" ,  "data-show-export":"true", 'data-export-types': "['csv','excel']"}