from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string
from authtools.admin import NamedUserAdmin
from django.contrib import admin
from ssme_activities.models import *
from ssme_activities.forms import UserCreationForm
from import_export import resources
from import_export.admin import ExportMixin, ImportExportModelAdmin


class CampaignBeneficiaryProductResource(resources.ModelResource):
    class Meta:
        model = CampaignBeneficiaryProduct
        fields = (
            "campaign_beneficiary__beneficiary__designation",
            "campaign_product__product__name",
            "dosage",
            "pourcentage_attendu",
        )


class CampaignBeneficiaryProductAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CampaignBeneficiaryProductResource
    list_display = (
        "campaign_beneficiary",
        "campaign_product",
        "dosage",
        "pourcentage_attendu",
    )
    list_filter = ("campaign_beneficiary__campaign",)


class CampaignBeneficiaryResource(resources.ModelResource):
    class Meta:
        model = CampaignBeneficiary
        fields = (
            "beneficiary__designation",
            "pourcentage_attendu", "order_in_sms")


class CampaignBeneficiaryAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CampaignBeneficiaryResource
    list_display = (
        "campaign",
        "beneficiary", "order_in_sms", "pourcentage_attendu")
    list_filter = ("campaign",)


class CampaignProductResource(resources.ModelResource):
    class Meta:
        model = CampaignProduct


class CampaignProductAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CampaignProductResource
    list_display = ("campaign", "product", "order_in_sms")
    list_filter = ("campaign",)


class CampaignCDSResource(resources.ModelResource):
    class Meta:
        model = CampaignCDS
        fields = (
            "cds__name",
            "population_cible",
            "cds__district__name",
            "cds__district__province__name",
        )


class CampaignCDSAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CampaignCDSResource
    list_display = (
        "campaign",
        "cds", "population_cible", "district", "province")
    search_fields = (
        "cds__name",
        "cds__district__name",
        "cds__district__province__name",
    )
    list_filter = (
        "cds__district__province__name",
        "campaign__name", "campaign__going_on")

    def district(self, obj):
        return obj.cds.district.name

    def province(self, obj):
        return obj.cds.district.province.name


class ReportResource(resources.ModelResource):
    class Meta:
        model = Report
        fields = (
            "id",
            "text",
            "concerned_date",
            "category",
            "cds__name",
            "cds__district__name",
            "cds__district__province__name",
        )


class ReportAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReportResource
    search_fields = (
        "text",
        "category",
        "cds__name",
        "cds__district__name",
        "cds__district__province__name",
    )
    list_filter = ("concerned_date", "reporting_date", "category")
    date_hierarchy = "reporting_date"
    list_display = (
        "id",
        "text",
        "concerned_date",
        "category",
        "cds",
        "district",
        "province",
    )

    def district(self, obj):
        return obj.cds.district.name

    def province(self, obj):
        return obj.cds.district.province.name


class ReportBeneficiaryResource(resources.ModelResource):
    class Meta:
        model = ReportBeneficiary
        fields = (
            "beneficiaries_per_product__campaign_beneficiary__beneficiary__designation",
            "beneficiaries_per_product__campaign_product__product__name",
            "received_number",
            "reception_date",
            "report__cds__name",
            "report__cds__district__name",
            "report__cds__district__province__name",
        )


class ReportBeneficiaryAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReportBeneficiaryResource
    search_fields = (
        "report__cds__name",
        "report__cds__district__name",
        "report__cds__district__province__name",
    )
    date_hierarchy = "reception_date"
    list_filter = ("reception_date", "report__reporting_date")
    list_display = (
        "beneficiary",
        "product",
        "received_number",
        "reception_date",
        "cds",
        "district",
        "province",
        "reporting_date",
    )

    def beneficiary(self, obj):
        return (
            obj.beneficiaries_per_product.campaign_beneficiary.beneficiary.designation
        )

    def product(self, obj):
        return obj.beneficiaries_per_product.campaign_product.product.name

    def cds(self, obj):
        return obj.report.cds.name

    def district(self, obj):
        return obj.report.cds.district.name

    def province(self, obj):
        return obj.report.cds.district.province.name

    def reporting_date(self, obj):
        return obj.report.reporting_date


# Test End
class ReportProductReceptionResource(resources.ModelResource):
    class Meta:
        model = ReportProductReception
        fields = (
            "campaign_product__product__name",
            "received_quantity",
            "reception_date",
            "report__cds__name",
            "report__cds__district__name",
            "report__cds__district__province__name",
        )


class ReportProductReceptionAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReportProductReceptionResource
    search_fields = (
        "campaign_product__product__name",
        "report__cds__name",
        "report__cds__district__name",
        "report__cds__district__province__name",
    )
    list_filter = ("reception_date", "report__reporting_date")
    list_display = (
        "product",
        "received_quantity",
        "reception_date",
        "cds",
        "district",
        "province",
    )

    def product(self, obj):
        return obj.campaign_product.product.name

    def cds(self, obj):
        return obj.report.cds.name

    def district(self, obj):
        return obj.report.cds.district.name

    def province(self, obj):
        return obj.report.cds.district.province.name


class ReportProductRemainStockResource(resources.ModelResource):
    class Meta:
        model = ReportProductRemainStock
        fields = (
            "campaign_product__product__name",
            "remain_quantity",
            "concerned_date",
            "report__cds__name",
            "report__cds__district__name",
            "report__cds__district__province__name",
        )


class ReportProductRemainStockAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReportProductRemainStockResource
    search_fields = (
        "campaign_product__product__name",
        "report__cds__name",
        "report__cds__district__name",
        "report__cds__district__province__name",
    )
    date_hierarchy = "concerned_date"
    list_filter = ("concerned_date", "report__reporting_date")
    list_display = (
        "product",
        "remain_quantity",
        "concerned_date",
        "cds",
        "district",
        "province",
    )

    def reports(self, obj):
        return obj.report.reception_date

    def product(self, obj):
        return obj.campaign_product.product.name

    def cds(self, obj):
        return obj.report.cds.name

    def district(self, obj):
        return obj.report.cds.district.name

    def province(self, obj):
        return obj.report.cds.district.province.name


class ReportStockOutResource(resources.ModelResource):
    class Meta:
        model = ReportStockOut
        fields = (
            "remaining_stock",
            "campaign_product__product__name",
            "report__cds__name",
            "report__cds__district__name",
            "report__cds__district__province__name",
        )


class ReportStockOutAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReportStockOutResource
    search_fields = (
        "campaign_product__product__name",
        "report__cds__name",
        "report__cds__district__name",
        "report__cds__district__province__name",
    )
    list_filter = ("report__cds__district__name",)
    list_display = ("cds", "product", "remaining_stock", "district", "province")

    def product(self, obj):
        return obj.campaign_product.product.name

    def cds(self, obj):
        return obj.report.cds.name

    def district(self, obj):
        return obj.report.cds.district.name

    def province(self, obj):
        return obj.report.cds.district.province.name


User = get_user_model()


class UserAdmin(NamedUserAdmin):
    """
    A UserAdmin that sends a password-reset email when creating a new user,
    unless a password was entered.
    """

    add_form = UserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "description": (
                    "Enter the new user's name and email address and click save."
                    " The user will be emailed a link allowing them to login to"
                    " the site and set their password."
                ),
                "fields": ("email", "name"),
            },
        ),
        (
            "Password",
            {
                "description": "Optionally, you may set the user's password here.",
                "fields": ("password1", "password2"),
                "classes": ("collapse", "collapse-closed"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change and (
            not form.cleaned_data["password1"] or not obj.has_usable_password()
        ):
            # Django's PasswordResetForm won't let us reset an unusable
            # password. We set it above super() so we don't have to save twice.
            obj.set_password(get_random_string())
            reset_password = True
        else:
            reset_password = False

        super(UserAdmin, self).save_model(request, obj, form, change)

        if reset_password:
            reset_form = PasswordResetForm({"email": obj.email})
            assert reset_form.is_valid()
            reset_form.save(
                request=request,
                use_https=request.is_secure(),
                subject_template_name="registration/account_creation_subject.txt",
                email_template_name="registration/account_creation_email.html",
            )


class ReporterResource(resources.ModelResource):
    class Meta:
        model = Reporter
        fields = (
            "phone_number",
            "supervisor_phone_number",
            "cds__name",
            "cds__district__name",
            "cds__district__province__name",
        )


class ReporterAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReporterResource
    search_fields = (
        "phone_number",
        "supervisor_phone_number",
        "cds__name",
        "cds__district__name",
        "cds__district__province__name",
    )
    list_display = (
        "phone_number",
        "cds",
        "supervisor_phone_number",
        "district",
        "province",
    )

    def district(self, obj):
        return obj.cds.district.name

    def province(self, obj):
        return obj.cds.district.province.name


class ProvinceResource(resources.ModelResource):
    class Meta:
        model = Province
        fields = ("name", "code")


class ProvinceAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProvinceResource
    search_fields = ("name", "code")
    list_display = ("name", "code")


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ("name", "unite_de_mesure")


class ProductAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProductResource
    search_fields = ("name", "unite_de_mesure")
    list_display = ("name", "unite_de_mesure")


class DistrictResource(resources.ModelResource):
    class Meta:
        model = District
        fields = ("name", "code", "province__name")


class DistrictAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = DistrictResource
    search_fields = ("name", "code", "province__name")
    list_display = ("name", "code", "province")

    def province(self, obj):
        return obj.province.name


class CDSResource(resources.ModelResource):
    class Meta:
        model = CDS
        fields = ("name", "code", "district__name", "district__province__name")


class CDSAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CDSResource
    search_fields = ("name", "code", "district__name", "district__province__name")
    list_display = ("name", "code", "district", "province")

    def province(self, obj):
        return obj.district.province.name

    def district(self, obj):
        return obj.district.name


class AllSupervisorsOnDistrictLevelResource(resources.ModelResource):
    class Meta:
        model = AllSupervisorsOnDistrictLevel
        fields = ("first_name", "last_name", "phone_number")


class AllSupervisorsOnDistrictLevelAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = AllSupervisorsOnDistrictLevelResource
    list_display = ("first_name", "last_name", "phone_number")
    search_fields = ("first_name", "last_name", "phone_number")


class DistrictSupervisorResource(resources.ModelResource):
    class Meta:
        model = DistrictSupervisor
        fields = (
            "district__name",
            "supervisor__phone_number",
            "district__province__name",
        )


class DistrictSupervisorAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = DistrictSupervisorResource
    list_display = ("district", "supervisor")
    list_filter = ("district__province__name",)
    search_fields = (
        "district__name",
        "supervisor__phone_number",
        "district__province__name",
        "supervisor__last_name",
        "supervisor__first_name",
    )


@admin.register(Campaign)
class CampaignAdmin(ImportExportModelAdmin):
    search_fields = ("id", "name", "start_date", "end_date", "going_on")
    list_display = ("id", "name", "start_date", "end_date", "going_on")
    list_display_links = ("id", "name")
    list_filter = ("going_on",)


@admin.register(Beneficiaire)
class BeneficiaireAdmin(ImportExportModelAdmin):
    search_fields = ("id", "designation", "nombre_mois_min", "nombre_mois_max")
    list_display = ("id", "designation", "nombre_mois_min", "nombre_mois_max")
    list_display_links = ("id", "designation")


admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(CDS, CDSAdmin)
admin.site.register(Reporter, ReporterAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CampaignBeneficiary, CampaignBeneficiaryAdmin)
admin.site.register(CampaignProduct, CampaignProductAdmin)
admin.site.register(CampaignBeneficiaryProduct, CampaignBeneficiaryProductAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(ReportBeneficiary, ReportBeneficiaryAdmin)
admin.site.register(ReportProductReception, ReportProductReceptionAdmin)
admin.site.register(ReportProductRemainStock, ReportProductRemainStockAdmin)
admin.site.register(Temporary)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(ReportStockOut, ReportStockOutAdmin)
admin.site.register(CampaignCDS, CampaignCDSAdmin)
admin.site.register(AllSupervisorsOnDistrictLevel, AllSupervisorsOnDistrictLevelAdmin)
admin.site.register(DistrictSupervisor, DistrictSupervisorAdmin)
