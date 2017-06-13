from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Product model """
    reception = serializers.SerializerMethodField()
    sortie = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "designation", "quantite_en_stock_central", "general_measuring_unit", 'reception', 'sortie', 'balance')

    def get_reception(self, obj):
        reception = ProductsReceptionReport.objects.filter(produit=obj, reception__report__facility__facility_level__name='Centrale').aggregate(reception=Coalesce(Sum('quantite_recue'), 0))
        return reception['reception']

    def get_sortie(self, obj):
        sortie = ProductsTranferReport.objects.filter(produit=obj, sortie__report__facility__facility_level__name='Centrale').aggregate(sortie=Coalesce(Sum('quantite_donnee'), 0))
        return sortie['sortie']

    def get_balance(self, obj):
        return 0