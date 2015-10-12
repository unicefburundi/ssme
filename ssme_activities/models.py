from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse


class ProfileUser(models.Model):
    MOH_LEVEL_CHOICES = (
        ('CEN', 'Central'),
        ('BPS', 'BPS'),
        ('BDS', 'BDS'),
        ('CDS', 'CDS'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    # The additional attributes we wish to include.
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    telephone = models.CharField(validators=[phone_regex], blank=True, help_text=_('The telephone to contact you.'), max_length=16)
    level= models.CharField(max_length=3, choices=MOH_LEVEL_CHOICES, blank=True, help_text=_('Either CDS, BDS, PBS, or Central level.'))
    moh_facility = models.IntegerField(null=True, blank=True, help_text=_('Code of the MoH facility'))

    def __unicode__(self):
        return self.user.name

    def get_absolute_url(self):
        return reverse('profile_user_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ('user',)


class Province(models.Model):
    '''In this model, we will store burundi provinces'''
    name = models.CharField(unique=True, max_length=20)
    code = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('province_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ('name',)

class District(models.Model):
    '''In this model, we will store districts'''
    province = models.ForeignKey(Province)
    name = models.CharField(unique=True, max_length=40)
    code = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('district_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ('name',)

class CDS(models.Model):
    '''In this model, we will store facilities'''
    district = models.ForeignKey(District)
    name = models.CharField(max_length=40)
    code = models.CharField(unique=True, max_length=6)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cds_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ('name',)

class Reporter(models.Model):
    '''In this model, we will store reporters'''
    cds = models.ForeignKey(CDS)
    phone_number = models.CharField(max_length=20)
    supervisor_phone_number = models.CharField(max_length=20)

    def __unicode__(self):
        return self.phone_number

    def get_absolute_url(self):
        return reverse('reporter_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ('phone_number',)

class Campaign(models.Model):
	'''In this model, we will store campaigns'''
	name = models.CharField(max_length=500)
	start_date = models.DateField()
	end_date = models.DateField()
	going_on = models.BooleanField(default=False)
	
	def __str__(self):
		return self.start_date.strftime("%B %d, %Y")

	def get_absolute_url(self):
		return reverse('ssme_activities.campaign_read', kwargs={'pk': self.id})

	class Meta:
		ordering = ('end_date',)

class Beneficiaire(models.Model):
	'''In this model, we will store every category of beneficiaries for ssme campaign'''
	designation = models.CharField(max_length=100)
	nombre_mois_min = models.IntegerField()
	nombre_mois_max = models.IntegerField()
	def __unicode__(self):
		return self.designation
	
	def get_absolute_url(self):
		return reverse('ssme_activities.beneficiaire_read', kwargs={'pk': self.id})
	
	class Meta:
		ordering = ('designation',)

class Product(models.Model):
    '''In this model, we will store names of medecines which may be used in ssme campaigns'''
    name = models.CharField(max_length=100)
    can_be_fractioned = models.BooleanField(default=False)
    unite_de_mesure = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ssme_activities.product_read', kwargs={'pk': self.id})

    class Meta:
        ordering = ('name',)

class CampaignBeneficiary(models.Model):
    '''With this model, we will be able to define and identify beneficiaries for a given ssme campaign'''
    campaign = models.ForeignKey(Campaign)
    beneficiary = models.ForeignKey(Beneficiaire)
    order_in_sms = models.IntegerField()

    class Meta:
        ordering = ('beneficiary',)
        unique_together = ('campaign', 'order_in_sms',)

    def __unicode__(self):
        return "%s from %s to %s " % (self.beneficiary.designation, self.campaign.start_date , self.campaign.end_date)

    def get_absolute_url(self):
        return reverse('ssme_activities.campaignbeneficiary_read', kwargs={'pk': self.id})


class CampaignBeneficiaryCDS(models.Model):
    campaign_beneficiary = models.ForeignKey(CampaignBeneficiary)
    cds = models.ForeignKey(CDS)
    population_attendu = models.IntegerField(null=True)
    population_obtenue = models.IntegerField(null=True)

class CampaignProduct(models.Model):
	'''With this model we will be able to define and identify concerned medecines for a given campaign'''
	campaign = models.ForeignKey(Campaign)
	product = models.ForeignKey(Product)
	order_in_sms = models.IntegerField()

	def __unicode__(self):
		return self.product.name

	def get_absolute_url(self):
		return reverse('ssme_activities.campaignproduct_read', kwargs={'pk': self.id})

	class Meta:
		ordering = ('product',)
		unique_together = ('campaign', 'order_in_sms',)

class CampaignBeneficiaryProduct(models.Model):
    '''With this model, we will be able to define and identify which medecines will be received by each beneficiary
    category and quantity for each Beneficiary'''
    campaign_beneficiary = models.ForeignKey(CampaignBeneficiary)
    campaign_product = models.ForeignKey(CampaignProduct)
    dosage = models.FloatField(null = True)

    def __unicode__(self):
        return self.campaign_beneficiary.beneficiary.designation

    def get_absolute_url(self):
        return reverse('ssme_activities.campaignbeneficiaryproduct_read', kwargs={'pk': self.id})

    class Meta:
        ordering = ('campaign_beneficiary',)

class Report(models.Model):
    '''In this model, we will store each report'''
    cds = models.ForeignKey(CDS)
    reporting_date = models.DateField()
    concerned_date = models.DateField()
    text = models.CharField(max_length=200)
    category = models.CharField(max_length=50)

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ('reporting_date',)

class ReportBeneficiary(models.Model):
    campaign_beneficiary = models.ForeignKey(CampaignBeneficiary)
    reception_date = models.DateField()
    received_number = models.IntegerField()
    report = models.ForeignKey(Report)

    def __unicode__(self):
        return self.report.text

    class Meta:
        ordering = ('reception_date',)

class ReportProductReception(models.Model):
    campaign_product = models.ForeignKey(CampaignProduct)
    reception_date = models.DateField()
    received_quantity = models.FloatField()
    report = models.ForeignKey(Report)

    def __unicode__(self):
        return self.report.text

    class Meta:
        ordering = ('reception_date',)

class ReportProductRemainStock(models.Model):
    campaign_product = models.ForeignKey(CampaignProduct)
    concerned_date = models.DateField()
    remain_quantity = models.FloatField()
    report = models.ForeignKey(Report)

    def __unicode__(self):
        return self.report.text

    class Meta:
        ordering = ('report',)


class Temporary(models.Model):
    '''
    This model will be used to temporary store a reporter who doesn't finish his self registration
    '''
    cds = models.ForeignKey(CDS)
    phone_number = models.CharField(max_length=20)
    supervisor_phone_number = models.CharField(max_length=20)

    def __unicode__(self):
        return self.phone_number

class CampaignCDS(models.Model):
	campaign = models.ForeignKey(Campaign)
	cds = models.ForeignKey(CDS)
	population_cible = models.IntegerField(null = True)
	enfant_moins_5_ans = models.IntegerField(null = True)

class ReportStockOut(models.Model):
	campaign_product = models.ForeignKey(CampaignProduct)
	report = models.ForeignKey(Report)
	remaining_stock = models.FloatField()

