from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string
from authtools.admin import NamedUserAdmin
from django.contrib import admin
from ssme_activities.models import  *
from ssme_activities.forms import UserCreationForm

User = get_user_model()

class UserAdmin(NamedUserAdmin):
    """
    A UserAdmin that sends a password-reset email when creating a new user,
    unless a password was entered.
    """
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'description': (
                "Enter the new user's name and email address and click save."
                " The user will be emailed a link allowing them to login to"
                " the site and set their password."
            ),
            'fields': ('email', 'name',),
        }),
        ('Password', {
            'description': "Optionally, you may set the user's password here.",
            'fields': ('password1', 'password2'),
            'classes': ('collapse', 'collapse-closed'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change and (not form.cleaned_data['password1'] or not obj.has_usable_password()):
            # Django's PasswordResetForm won't let us reset an unusable
            # password. We set it above super() so we don't have to save twice.
            obj.set_password(get_random_string())
            reset_password = True
        else:
            reset_password = False

        super(UserAdmin, self).save_model(request, obj, form, change)

        if reset_password:
            reset_form = PasswordResetForm({'email': obj.email})
            assert reset_form.is_valid()
            reset_form.save(
                request=request,
                use_https=request.is_secure(),
                subject_template_name='registration/account_creation_subject.txt',
                email_template_name='registration/account_creation_email.html',
            )

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
admin.site.register(Temporary)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(ReportStockOut)
admin.site.register(CampaignCDS)
