from django.contrib import admin
from ssme_activities.models import  *

# Register your models here.

admin.site.register(Province)
admin.site.register(District)
admin.site.register(CDS)
admin.site.register(Reporter)
admin.site.register(Campaign)
admin.site.register(Beneficiaire)
admin.site.register(Product)
admin.site.register(CampaignBeneficiary)
admin.site.register(CampaignProduct)
admin.site.register(CampaignBeneficiaryProduct)
admin.site.register(Report)
admin.site.register(ReportBeneficiary)
admin.site.register(ReportProductReception)
admin.site.register(ReportProductRemainStock)

