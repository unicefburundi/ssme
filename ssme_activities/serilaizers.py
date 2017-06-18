from rest_framework import serializers
from ssme_activities.models import Province, District, CDS, Report, Campaign
import datetime

days = Campaign.objects.filter(going_on=True).values('start_date', 'end_date')


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
        return rappors.count()

    def get_stock_finals(self, obj):
        rappors = Report.objects.filter(category="STOCK_FINAL", cds__district__province=obj, concerned_date__range=[days[0]['start_date'], days[0]['end_date']]).distinct()
        if self.context and "dates" in self.context:
            return Report.objects.filter(category="STOCK_FINAL", cds__district__province=obj, reporting_date=datetime.datetime.strptime(self.context["dates"], '%Y-%m-%d')).count()
        return rappors.count()

    def get_beneficiaires(self, obj):
        rappors = Report.objects.filter(category="BENEFICIAIRE", cds__district__province=obj, concerned_date__range=[days[0]['start_date'], days[0]['end_date']]).distinct()
        if self.context and "dates" in self.context:
            return Report.objects.filter(category="BENEFICIAIRE", cds__district__province=obj, reporting_date=datetime.datetime.strptime(self.context["dates"], '%Y-%m-%d')).count()
        return rappors.count()

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
        return rappors.count()

    def get_stock_finals(self, obj):
        rappors = Report.objects.filter(category="STOCK_FINAL", cds__district=obj, concerned_date__range=[days[0]['start_date'], days[0]['end_date']]).distinct()
        if self.context and "dates" in self.context:
            return Report.objects.filter(category="STOCK_FINAL", cds__district=obj, reporting_date=datetime.datetime.strptime(self.context["dates"], '%Y-%m-%d')).count()
        return rappors.count()

    def get_beneficiaires(self, obj):
        rappors = Report.objects.filter(category="BENEFICIAIRE", cds__district=obj, concerned_date__range=[days[0]['start_date'], days[0]['end_date']]).distinct()
        if self.context and "dates" in self.context:
            return Report.objects.filter(category="BENEFICIAIRE", cds__district=obj, reporting_date=datetime.datetime.strptime(self.context["dates"], '%Y-%m-%d')).count()
        return rappors.count()

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
        return rappors.count()

    def get_stock_finals(self, obj):
        rappors = Report.objects.filter(category="STOCK_FINAL", cds=obj, concerned_date__range=[days[0]['start_date'], days[0]['end_date']]).distinct()
        if self.context and "dates" in self.context:
            return Report.objects.filter(category="STOCK_FINAL", cds=obj, reporting_date=datetime.datetime.strptime(self.context["dates"], '%Y-%m-%d')).count()
        return rappors.count()

    def get_beneficiaires(self, obj):
        rappors = Report.objects.filter(category="BENEFICIAIRE", cds=obj, concerned_date__range=[days[0]['start_date'], days[0]['end_date']]).distinct()
        if self.context and "dates" in self.context:
            return Report.objects.filter(category="BENEFICIAIRE", cds=obj, reporting_date=datetime.datetime.strptime(self.context["dates"], '%Y-%m-%d')).count()
        return rappors.count()

    def get_facilities(self, obj):
        facilities = CDS.objects.filter(pk=obj.pk).distinct().count()
        return facilities


class CampaignSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Campaign model """
    days = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = ("id", "name", "start_date", "end_date", "going_on", "days")

    def get_days(self, obj):
        lesdates = [datetime.date.fromordinal(i) for i in range(obj.start_date.toordinal(), obj.end_date.toordinal()+1)]
        return dict(list(enumerate(lesdates)))
