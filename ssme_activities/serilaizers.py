from rest_framework import serializers
from ssme_activities.models import Province, District, CDS, Report, Campaign, ReportBeneficiary, CampaignBeneficiaryProduct
import datetime
from django.db.models import F, Sum
from django.db.models.functions import Concat, Substr
from django.db.models import CharField, Value as V
days = Campaign.objects.filter(going_on=True).values('start_date', 'end_date')

#get average if no campaign day is selected
campaigndays = (datetime.datetime.strptime(days[0]['end_date'].isoformat(), "%Y-%m-%d").date() - datetime.datetime.strptime(days[0]['start_date'].isoformat(), "%Y-%m-%d").date()).days


def get_report_by_code(request, code, model):
    queryset = model.objects.all()
    if not queryset:
        return queryset
    if not code:
        return queryset
    if len(code) <= 2:
        return queryset.filter(report__cds__district__province__code=int(code)).order_by('report__concerned_date')
    if len(code) > 2 and len(code) <= 4:
        return queryset.filter(report__cds__district__code=int(code)).order_by('report__concerned_date')
    if len(code) > 4:
        return queryset.filter(report__cds__code=code).order_by('report__concerned_date')


class ProvinceSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Province model """
    stock_debut_semaine = serializers.SerializerMethodField()
    stock_finals = serializers.SerializerMethodField()
    beneficiaires = serializers.SerializerMethodField()
    facilities = serializers.SerializerMethodField()

    class Meta:
        model = Province
        fields = ("id", "name", "code", "stock_debut_semaine", "stock_finals", "facilities", "beneficiaires")

    def get_stock_debut_semaine(self, obj):
        rappors = Report.objects.filter(category="STOCK_DEBUT_SEMAINE", cds__district__province=obj, concerned_date__range=[days[0]['start_date'], days[0]['end_date']]).distinct()
        if self.context and "dates" in self.context:
            return Report.objects.filter(category="STOCK_DEBUT_SEMAINE", cds__district__province=obj, reporting_date=datetime.datetime.strptime(self.context["dates"], '%Y-%m-%d')).count()
        return rappors.count()/campaigndays

    def get_stock_finals(self, obj):
        rappors = Report.objects.filter(category="STOCK_FINAL", cds__district__province=obj, concerned_date__range=[days[0]['start_date'], days[0]['end_date']]).distinct()
        if self.context and "dates" in self.context:
            return Report.objects.filter(category="STOCK_FINAL", cds__district__province=obj, reporting_date=datetime.datetime.strptime(self.context["dates"], '%Y-%m-%d')).count()
        return rappors.count()/campaigndays

    def get_beneficiaires(self, obj):
        rappors = Report.objects.filter(category="BENEFICIAIRE", cds__district__province=obj, concerned_date__range=[days[0]['start_date'], days[0]['end_date']]).distinct()
        if self.context and "dates" in self.context:
            return Report.objects.filter(category="BENEFICIAIRE", cds__district__province=obj, reporting_date=datetime.datetime.strptime(self.context["dates"], '%Y-%m-%d')).count()
        return rappors.count()/campaigndays

    def get_facilities(self, obj):
        facilities = CDS.objects.filter(district__province=obj).distinct().count()
        return facilities


class DistrictSerializer(serializers.ModelSerializer):
    """ Serializer to represent the District model """
    stock_finals = serializers.SerializerMethodField()
    stock_debut_semaine = serializers.SerializerMethodField()
    beneficiaires = serializers.SerializerMethodField()
    facilities = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = ("id", "name", "code", "province", "stock_debut_semaine", "stock_finals", "facilities", "beneficiaires")

    def get_stock_debut_semaine(self, obj):
        rappors = Report.objects.filter(category="STOCK_DEBUT_SEMAINE", cds__district=obj, concerned_date__range=[days[0]['start_date'], days[0]['end_date']]).distinct()
        if self.context and "dates" in self.context:
            return Report.objects.filter(category="STOCK_DEBUT_SEMAINE", cds__district=obj, reporting_date=datetime.datetime.strptime(self.context["dates"], '%Y-%m-%d')).count()
        return rappors.count()/campaigndays

    def get_stock_finals(self, obj):
        rappors = Report.objects.filter(category="STOCK_FINAL", cds__district=obj, concerned_date__range=[days[0]['start_date'], days[0]['end_date']]).distinct()
        if self.context and "dates" in self.context:
            return Report.objects.filter(category="STOCK_FINAL", cds__district=obj, reporting_date=datetime.datetime.strptime(self.context["dates"], '%Y-%m-%d')).count()
        return rappors.count()/campaigndays

    def get_beneficiaires(self, obj):
        rappors = Report.objects.filter(category="BENEFICIAIRE", cds__district=obj, concerned_date__range=[days[0]['start_date'], days[0]['end_date']]).distinct()
        if self.context and "dates" in self.context:
            return Report.objects.filter(category="BENEFICIAIRE", cds__district=obj, reporting_date=datetime.datetime.strptime(self.context["dates"], '%Y-%m-%d')).count()
        return rappors.count()/campaigndays

    def get_facilities(self, obj):
        facilities = CDS.objects.filter(district=obj).distinct().count()
        return facilities


class CDSSerializer(serializers.ModelSerializer):
    """ Serializer to represent the CDS model """
    stock_debut_semaine = serializers.SerializerMethodField()
    beneficiaires = serializers.SerializerMethodField()
    stock_finals = serializers.SerializerMethodField()
    facilities = serializers.SerializerMethodField()

    class Meta:
        model = CDS
        fields = ("id", "name", "code", "district", "stock_debut_semaine", "stock_finals", "facilities", "beneficiaires")

    def get_stock_debut_semaine(self, obj):
        rappors = Report.objects.filter(category="STOCK_DEBUT_SEMAINE", cds=obj, concerned_date__range=[days[0]['start_date'], days[0]['end_date']]).distinct()
        if self.context and "dates" in self.context:
            return Report.objects.filter(category="STOCK_DEBUT_SEMAINE", cds=obj, reporting_date=datetime.datetime.strptime(self.context["dates"], '%Y-%m-%d')).count()
        return rappors.count()/campaigndays

    def get_stock_finals(self, obj):
        rappors = Report.objects.filter(category="STOCK_FINAL", cds=obj, concerned_date__range=[days[0]['start_date'], days[0]['end_date']]).distinct()
        if self.context and "dates" in self.context:
            return Report.objects.filter(category="STOCK_FINAL", cds=obj, reporting_date=datetime.datetime.strptime(self.context["dates"], '%Y-%m-%d')).count()
        return rappors.count()/campaigndays

    def get_beneficiaires(self, obj):
        rappors = Report.objects.filter(category="BENEFICIAIRE", cds=obj, concerned_date__range=[days[0]['start_date'], days[0]['end_date']]).distinct()
        if self.context and "dates" in self.context:
            return Report.objects.filter(category="BENEFICIAIRE", cds=obj, reporting_date=datetime.datetime.strptime(self.context["dates"], '%Y-%m-%d')).count()
        return rappors.count()/campaigndays

    def get_facilities(self, obj):
        facilities = CDS.objects.filter(pk=obj.pk).distinct().count()
        return facilities


class CampaignSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Campaign model """
    days = serializers.SerializerMethodField()
    benefs = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = ("id", "name", "start_date", "end_date", "going_on", "days", "benefs")

    def get_days(self, obj):
        lesdates = [datetime.date.fromordinal(i) for i in range(obj.start_date.toordinal(), obj.end_date.toordinal()+1)]
        return dict(list(enumerate(lesdates)))

    def get_benefs(self, obj):
        dates_benef = ReportBeneficiary.objects.values('reception_date').distinct()
        queryset_benef = get_report_by_code(self.context.get("request"), self.context.get("mycode"), ReportBeneficiary)
        body_benef = []
        headers_benef = CampaignBeneficiaryProduct.objects.all().annotate(beneficiaires=Concat(Substr(F('campaign_product__product__name'), 1, 10), V(' ('), Substr(F('campaign_beneficiary__beneficiary__designation'), 1, 5), V(')'), output_field=CharField())).values('beneficiaires', 'id').order_by('id')
        for i in dates_benef:
            res, ress = i, {}
            for t in headers_benef:
                ress = queryset_benef.annotate(beneficiaires=F('beneficiaries_per_product__campaign_product__product__name')).filter(reception_date=i['reception_date'], beneficiaries_per_product=t['id']).values('received_number').aggregate(total=Sum('received_number'))
                if not ress['total']:
                    res.update({t['beneficiaires']: 0})
                else:
                    res.update({t['beneficiaires']: ress['total']})
            body_benef.append(res)
        return body_benef
