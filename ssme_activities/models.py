#!/usr/bin/python
# -*- coding: utf-8  -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
import datetime


class ProfileUser(models.Model):
    MOH_LEVEL_CHOICES = (
        ("CEN", "Central"),
        ("BPS", "BPS"),
        ("BDS", "BDS"),
        ("CDS", "CDS"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    # The additional attributes we wish to include.
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message=_(
            "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        ),
    )
    telephone = models.CharField(
        "téléphone",
        validators=[phone_regex],
        blank=True,
        help_text=_("The telephone to contact you."),
        max_length=16,
    )
    level = models.CharField(
        "niveau",
        max_length=3,
        choices=MOH_LEVEL_CHOICES,
        blank=True,
        help_text=_("Either CDS, BDS, PBS, or Central level."),
    )
    moh_facility = models.CharField(
        "code",
        max_length=8,
        null=True,
        blank=True,
        help_text=_("Code of the MoH facility"),
    )

    def __unicode__(self):
        return self.user.name

    def get_absolute_url(self):
        return reverse("profile_user_detail", kwargs={"pk": self.id})

    class Meta:
        ordering = ("user",)


class Province(models.Model):
    """In this model, we will store burundi provinces"""

    name = models.CharField("nom", unique=True, max_length=20)
    code = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("province_detail", kwargs={"pk": self.id})

    class Meta:
        ordering = ("name",)


class District(models.Model):
    """In this model, we will store districts"""

    province = models.ForeignKey(Province, verbose_name="province")
    name = models.CharField("nom", unique=True, max_length=40)
    code = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("district_detail", kwargs={"pk": self.id})

    class Meta:
        ordering = ("name",)


class CDS(models.Model):
    """In this model, we will store facilities"""

    district = models.ForeignKey(District, verbose_name="district")
    name = models.CharField("nom", max_length=40)
    code = models.CharField(unique=True, max_length=6)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cds_detail", kwargs={"pk": self.id})

    class Meta:
        ordering = ("name",)


class Reporter(models.Model):
    """In this model, we will store reporters"""

    cds = models.ForeignKey(CDS)
    phone_number = models.CharField(max_length=20)
    supervisor_phone_number = models.CharField(max_length=20)

    def __unicode__(self):
        return self.phone_number

    def get_absolute_url(self):
        return reverse("reporter_detail", kwargs={"pk": self.id})

    class Meta:
        ordering = ("phone_number",)


class Campaign(models.Model):
    """In this model, we will store campaigns"""

    name = models.CharField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    going_on = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ssme_activities.campaign_read", kwargs={"pk": self.id})

    class Meta:
        ordering = ("end_date",)


class Beneficiaire(models.Model):
    """In this model, we will store every category of beneficiaries for ssme campaign"""

    designation = models.CharField(max_length=100)
    nombre_mois_min = models.IntegerField(null=True, blank=True)
    nombre_mois_max = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.designation

    def get_absolute_url(self):
        return reverse("ssme_activities.beneficiaire_read", kwargs={"pk": self.id})

    class Meta:
        ordering = ("designation",)


class Product(models.Model):
    """In this model, we will store names of medecines which may be used in ssme campaigns"""

    name = models.CharField(max_length=100)
    can_be_fractioned = models.BooleanField(default=False)
    unite_de_mesure = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ssme_activities.product_read", kwargs={"pk": self.id})

    class Meta:
        ordering = ("name",)


class CampaignBeneficiary(models.Model):
    """With this model, we will be able to define and identify beneficiaries for a given ssme campaign"""

    campaign = models.ForeignKey(Campaign)
    beneficiary = models.ForeignKey(Beneficiaire)
    order_in_sms = models.IntegerField()
    pourcentage_attendu = models.FloatField(default=100.0, null=True)

    class Meta:
        ordering = ("beneficiary",)
        unique_together = ("campaign", "beneficiary")

    def __unicode__(self):
        return "{} dans {}".format(
            self.beneficiary.designation, self.campaign)

    def get_absolute_url(self):
        return reverse(
            "ssme_activities.campaignbeneficiary_read", kwargs={"pk": self.id}
        )


class CampaignBeneficiaryCDS(models.Model):
    campaign = models.ForeignKey(Campaign)
    cds = models.ForeignKey(CDS)
    population_attendu = models.IntegerField(null=True)
    population_obtenue = models.IntegerField(null=True)

    def __unicode__(self):
        return "{0} on {1}".format(self.beneficiary.designation, self.cds.name)


class CampaignProduct(models.Model):
    """With this model we will be able to define and identify concerned medecines for a given campaign"""

    campaign = models.ForeignKey(Campaign)
    product = models.ForeignKey(Product)
    order_in_sms = models.IntegerField()

    def __unicode__(self):
        return "{} dans {}".format(
            self.product.name, self.campaign)

    def get_absolute_url(self):
        return reverse("ssme_activities.campaignproduct_read", kwargs={"pk": self.id})

    class Meta:
        ordering = ("product",)
        unique_together = ("campaign", "product", "order_in_sms")


class CampaignBeneficiaryProduct(models.Model):
    """ With this model, we will be able to 
    define and identify which medecines will be received by each beneficiary
    category and quantity for each Beneficiary """

    campaign_beneficiary = models.ForeignKey(
        CampaignBeneficiary,
        related_name='campaign_beneficiary')
    campaign_product = models.ForeignKey(
        CampaignProduct,
        related_name='campaign_product')
    dosage = models.FloatField(null=True, default=0.0)
    pourcentage_attendu = models.FloatField(default=0.0, null=True)
    order_in_sms = models.IntegerField()

    def __unicode__(self):
        return self.campaign_beneficiary.beneficiary.designation

    def get_absolute_url(self):
        return reverse(
            "ssme_activities.campaignbeneficiaryproduct_read", kwargs={"pk": self.id}
        )

    class Meta:
        ordering = ("campaign_beneficiary",)
        unique_together = ("campaign_beneficiary", "campaign_product", "order_in_sms")


class Report(models.Model):
    """In this model, we will store each report"""

    cds = models.ForeignKey(CDS)
    reporting_date = models.DateField(null=True, blank=True)
    concerned_date = models.DateField()
    text = models.CharField(max_length=200)
    category = models.CharField(max_length=50)

    def __unicode__(self):
        return self.text

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        self.reporting_date = datetime.datetime.now().date()
        return super(Report, self).save(*args, **kwargs)

    class Meta:
        ordering = ("reporting_date",)


class ReportBeneficiary(models.Model):
    # The below fied will be removed
    campaign_beneficiary = models.ForeignKey(CampaignBeneficiary)
    beneficiaries_per_product = models.ForeignKey(CampaignBeneficiaryProduct)
    reception_date = models.DateField()
    received_number = models.IntegerField(null=True)
    report = models.ForeignKey(Report, null=True)

    def __unicode__(self):
        return self.report.text

    class Meta:
        get_latest_by = "id"


class ReportProductReception(models.Model):
    campaign_product = models.ForeignKey(CampaignProduct)
    reception_date = models.DateField()
    received_quantity = models.FloatField(null=True)
    report = models.ForeignKey(Report, null=True)

    def __unicode__(self):
        return self.report.text

    class Meta:
        get_latest_by = "id"


class ReportProductRemainStock(models.Model):
    campaign_product = models.ForeignKey(CampaignProduct)
    concerned_date = models.DateField()
    remain_quantity = models.FloatField(null=True)
    report = models.ForeignKey(Report, null=True)

    def __unicode__(self):
        return self.report.text

    class Meta:
        get_latest_by = "id"


class Temporary(models.Model):
    """
    This model will be used to temporary store a reporter who doesn't finish his self registration
    """

    cds = models.ForeignKey(CDS)
    phone_number = models.CharField(max_length=20)
    supervisor_phone_number = models.CharField(max_length=20)

    def __unicode__(self):
        return self.phone_number


class CampaignCDS(models.Model):
    campaign = models.ForeignKey(Campaign)
    cds = models.ForeignKey(CDS)
    population_cible = models.IntegerField(null=True)
    enfant_moins_5_ans = models.IntegerField(null=True)

    def __unicode__(self):
        return "{0} expects {1}".format(self.cds, self.population_cible)


class ReportStockOut(models.Model):
    campaign_product = models.ForeignKey(CampaignProduct)
    report = models.ForeignKey(Report)
    remaining_stock = models.FloatField()

    def __unicode__(self):
        return "{0} report stock-out of {1} with a remaining stock {2}".format(
            self.report.cds, self.campaign_product.product.name, self.remaining_stock
        )


class AllSupervisorsOnDistrictLevel(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    class Meta:
        ordering = ['first_name']


class DistrictSupervisor(models.Model):
    district = models.ForeignKey(District)
    supervisor = models.ForeignKey(AllSupervisorsOnDistrictLevel)

    def __unicode__(self):
        return "{0} {1} Supervise {2}".format(
            self.supervisor.first_name, self.supervisor.last_name, self.district.name
        )
