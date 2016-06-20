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
    beneficiaries_per_product = tables.Column(accessor='beneficiaries_per_product.campaign_product')
    date = tables.Column(attrs={"th": {"rowspan": 2}})
    jour = tables.Column(attrs={"th": {"rowspan": 2}})
    campaign_beneficiary = tables.Column(attrs={"th": {"colspan": 2}})
    id = tables.Column(attrs={"th": {"rowspan": 2}})

    class Meta:
        model = ReportBeneficiary
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" ,  "data-show-export":"true", 'data-export-types': "['csv','excel']"}
        exclude = ( 'report',)
        row_attrs = {
            'data-id': lambda record: record.pk
        }
        sequence = ('id', 'jour', 'date', '...')