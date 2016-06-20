from django import forms
from authtools.forms import UserCreationForm
from betterforms.multiform import MultiModelForm
from collections import OrderedDict
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from ssme_activities.models import *
from ssme.context_processor import myfacility


class UserCreationForm(UserCreationForm):
    """
    A UserCreationForm with optional password inputs.
    """

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(UserCreationForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2

class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = '__all__'

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = '__all__'

class CDSForm(forms.ModelForm):
    class Meta:
        model = CDS
        fields = '__all__'

#User

class UserProfileForm2(forms.ModelForm):
    class Meta:
        model = ProfileUser
        exclude = ('user',)

class UserCreationMultiForm(MultiModelForm):
    form_classes = OrderedDict((
        ('user', UserCreationForm),
        ('profile', UserProfileForm2),
    ))

# Campaign

MAX_ELEMENTS = 10

ProductsFormSet = inlineformset_factory(Campaign,
    CampaignProduct,
    can_delete=True,
    fields='__all__',
    extra=MAX_ELEMENTS)

BeneficiaryFormSet = inlineformset_factory(Campaign,
    CampaignBeneficiary,
    can_delete=True,
    fields='__all__',
    extra=MAX_ELEMENTS)

CDSCampaignFormSet = inlineformset_factory(Campaign,
    CampaignBeneficiaryCDS,
    can_delete=True,
    fields='__all__',
    extra=MAX_ELEMENTS)

class CampaignForm1(forms.ModelForm):
    start_date = forms.DateField(input_formats=['%d/%m/%Y'])
    end_date = forms.DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Campaign
        fields = '__all__'


class CampaignForm2(forms.ModelForm):
    class Meta:
        model = CampaignProduct
        fields = '__all__'



class CampaignForm3(forms.ModelForm):
    class Meta:
        model = CampaignBeneficiary
        fields = '__all__'

class ProductForm(forms.ModelForm):
    DOSAGE_CHOICES = (
        ('Dose', _('Dose')),
        ('Comprime', _('Pill')),
        ('Injection', _('Injection')),
    )
    unite_de_mesure = forms.ChoiceField(required=False, choices=DOSAGE_CHOICES)

    class Meta:
        model = Product
        fields = '__all__'

class   SearchBenef(forms.Form):
    province = forms.ModelChoiceField(queryset=Province.objects.all())
    district = forms.ModelChoiceField(queryset=District.objects.all())
    CDS = forms.ModelChoiceField(queryset=CDS.objects.all())

    def __init__(self, request, *args, **kwargs):
        super(SearchBenef, self).__init__(*args, **kwargs)
        import ipdb; ipdb.set_trace()
        moh_facility = myfacility(request)
        if not moh_facility['mylevel'] in ['CEN', 'Central']:
            if moh_facility['mylevel'] in ['CDS']:
                self.fields['CDS'].queryset = CDS.objects.filter(code=moh_facility['mycode'])
                self.fields['district'].queryset = District.objects.filter(code=moh_facility['mycode'])
