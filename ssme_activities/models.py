from django.db import models

class User(models.Model):
    nom = models.CharField(max_length=40)
    prenom = models.CharField(max_length=40)
    login = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    level = models.CharField(max_length=20)
    
class Province(models.Model):
    '''In this model, we will store burundi provinces'''
    name = models.CharField(unique=True, max_length=20)
    code = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.name

class District(models.Model):
    '''In this model, we will store districts'''
    province = models.ForeignKey(Province)
    name = models.CharField(unique=True, max_length=40)
    code = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.name

class CDS(models.Model):
    '''In this model, we will store facilities'''
    district = models.ForeignKey(District)
    name = models.CharField(max_length=40)
    code = models.CharField(unique=True, max_length=6)
    def __unicode__(self):
        return self.name

class Report(models.Model):
    '''In this model, we will store each report'''
    creation_date = models.DateField()
    cds = models.ForeignKey(CDS)
    text = models.CharField(max_length=200)

class Reporter(models.Model):
    '''In this model, we will store reporters'''
    phone_number = models.CharField(max_length=20)
    supervisor_phone_number = models.CharField(max_length=20)

class Campaign(models.Model):
    '''In this model, we will store campaigns'''
    start_date = models.DateField()
    end_date = models.DateField()
    open = models.BooleanField(default=False)

class Beneficiaire(models.Model):
    '''In this model, we will store every category of beneficiaries for ssme campaign'''
    designation = models.CharField(max_length=100)
    priority = models.IntegerField()

class Product(models.Model):
    '''In this model, we will store names of medecines which may be used in ssme campaigns'''
    models.CharField(max_length=200)
    priority = models.IntegerField()
    can_be_fractioned = models.BooleanField(default=False)

class CampaignBeneficiary(models.Model):
    '''With this model, we will be able to define and identify beneficiaries for a given ssme campaign'''
    campaign = models.ForeignKey(Campaign)
    beneficairy = models.ForeignKey(Beneficiaire)
    order_in_sms = models.IntegerField()
    class Meta:
        unique_together = ('campaign', 'beneficairy', 'order_in_sms',)

class CampaignProduct(models.Model):
    '''With this model we will be able to define and identify concerned medecines for a given campaign'''
    campaign = models.ForeignKey(Campaign)
    product = models.ForeignKey(Product)
    order_in_sms = models.IntegerField()
    class Meta:
        unique_together = ('campaign', 'product', 'order_in_sms',)

class CampaignBeneficiaryProduct(models.Model):
    '''With this model, we will be able to define and identify which medecines will be received by each beneficiary 
    category and quantity for each Beneficiary'''
    camapaign_beneficiary = models.ForeignKey(CampaignBeneficiary)
    campaign_product = models.ForeignKey(CampaignProduct)
    dosage = models.FloatField()

class CampaignCDS(models.Model):
    '''With this model, we will be able to define and identify facilicties concerned by a given ssme campaign'''
    campaign = models.ForeignKey(Campaign)
    cds = models.ForeignKey(CDS)
    
class CampaignCDSBeneficiary(models.Model):
    '''With this model, we will be able to define and identify expected beneficiaries at a given facility and given campaign'''
    campaign_cds = models.ForeignKey(CampaignCDS)
    beneficiary = models.ForeignKey(CampaignBeneficiary)
    expected_number = models.IntegerField()

class ReportBeneficiary(models.Model):
    campaign_cds_beneficiary = models.ForeignKey(CampaignCDSBeneficiary)
    reception_date = models.DateField()
    received_number = models.IntegerField()

class CampaignCDSProduit(models.Model):
    campaign_cds = models.ForeignKey(CampaignCDS)
    produit = models.ForeignKey(Product)

class ReportProductReception(models.Model):
    campaign_cds_product = models.ForeignKey(CampaignCDSProduit)
    reception_date = models.DateField()
    received_quantity = models.IntegerField()
    
class ReportProductStock(models.Model):
    campaign_cds_product = models.ForeignKey(CampaignCDSProduit)
    concerned_date = models.DateField()
    remain_quantity = models.IntegerField()
