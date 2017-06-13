from rest_framework import serializers
from ssme_activities.models import Province, District, CDS


class ProvinceSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Province model """

    class Meta:
        model = Province
        fields = ("id", "name", "code")

    # def get_reception(self, obj):
    #     reception = ProvincesReceptionReport.objects.filter(produit=obj, reception__report__facility__facility_level__name='Centrale').aggregate(reception=Coalesce(Sum('quantite_recue'), 0))
    #     return reception['reception']

    # def get_sortie(self, obj):
    #     sortie = ProvincesTranferReport.objects.filter(produit=obj, sortie__report__facility__facility_level__name='Centrale').aggregate(sortie=Coalesce(Sum('quantite_donnee'), 0))
    #     return sortie['sortie']

    # def get_balance(self, obj):
    #     return 0


class DistrictSerializer(serializers.ModelSerializer):
    """ Serializer to represent the District model """

    class Meta:
        model = District
        fields = ("id", "name", "code", "province")


class CDSSerializer(serializers.ModelSerializer):
    """ Serializer to represent the CDS model """

    class Meta:
        model = CDS
        fields = ("id", "name", "code", "district")
