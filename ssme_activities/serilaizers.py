from rest_framework import serializers
from ssme_activities.models import Province, District, CDS, Report


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
        rappors = Report.objects.filter(category="STOCK_DEBUT_SEMAINE", cds__district__province=obj).distinct().count()

        return rappors

    def get_stock_finals(self, obj):
        rappors = Report.objects.filter(category="STOCK_FINAL", cds__district__province=obj).distinct().count()

        return rappors

    def get_beneficiaires(self, obj):
        rappors = Report.objects.filter(category="BENEFICIAIRE", cds__district__province=obj).distinct().count()

        return rappors

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
        rappors = Report.objects.filter(category="STOCK_DEBUT_SEMAINE", cds__district=obj).distinct().count()

        return rappors

    def get_stock_finals(self, obj):
        rappors = Report.objects.filter(category="STOCK_FINAL", cds__district=obj).distinct().count()

        return rappors

    def get_beneficiaires(self, obj):
        rappors = Report.objects.filter(category="BENEFICIAIRE", cds__district=obj).distinct().count()

        return rappors

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
        rappors = Report.objects.filter(category="STOCK_DEBUT_SEMAINE", cds=obj).distinct().count()

        return rappors

    def get_stock_finals(self, obj):
        rappors = Report.objects.filter(category="STOCK_FINAL", cds=obj).distinct().count()

        return rappors

    def get_beneficiaires(self, obj):
        rappors = Report.objects.filter(category="BENEFICIAIRE", cds=obj).distinct().count()

        return rappors

    def get_facilities(self, obj):
        facilities = CDS.objects.filter(pk=obj.pk).distinct().count()
        return facilities
