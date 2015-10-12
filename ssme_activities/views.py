from django.shortcuts import render
from ssme_activities.models import *
from ssme_activities.forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from smartmin.views import *
from formtools.wizard.views import SessionWizardView
def dashboard(request):
    return render(request, 'base_layout.html')

def moh_facility(request):
    cds_form = CDSForm
    district_form = DistrictForm
    province_form = ProvinceForm
    return render(request, 'ssme_activities/moh_facility.html', {'cds_form':cds_form, 'district_form':district_form, 'province_form':province_form})

def profile_user(request):
    profile_form = UserCreationMultiForm
    return render(request, 'ssme_activities/profile_user.html', {'profile_form':profile_form})

def campaigns(request):
    return render(request, 'ssme_activities/campaigns.html')

def beneficiaries(request):
    return render(request, 'ssme_activities/beneficiaries.html')

#Province
class ProvinceCreateView(CreateView):
    model = Province
    form_class = ProvinceForm

class ProvinceListView(ListView):
    model = Province
    paginate_by = 25

class ProvinceDetailView(DetailView):
    model = Province

# District
class DistrictCreateView(CreateView):
    model = District
    form_class = DistrictForm

class DistrictListView(ListView):
    model = District
    paginate_by = 25

class DistrictDetailView(DetailView):
    model = District

# CDS
class CDSCreateView(CreateView):
    model = CDS
    form_class = CDSForm

class CDSListView(ListView):
    model = CDS
    paginate_by = 25

class CDSDetailView(DetailView):
    model = CDS

# ProfileUser
class UserSignupView(CreateView):
    form_class = UserCreationMultiForm
    template_name = 'registration/create_profile.html'

    def get_success_url(self, user):
        return reverse( 'profile_user_detail', kwargs = {'pk': user.id},)

    def form_valid(self, form):
        # Save the user first, because the profile needs a user before it
        # can be saved.
        user = form['user'].save()
        profile = form['profile'].save(commit=False)
        group = Group.objects.get_or_create(name=form['profile'].cleaned_data['level'])
        user.groups.add(group[0])
        profile.user = user
        profile.save()
        return redirect(self.get_success_url(user))

class ProfileUserListView(ListView):
    model = ProfileUser
    paginate_by = 25

class ProfileUserDetailView(DetailView):
    model = ProfileUser
    slug_field = "user"

class ProfileUserUpdateView(UpdateView):
    model = ProfileUser
    fields = ('telephone',)
    exclude = ('user',)

# Reporter
class ReporterListView(ListView):
    model = Reporter
    paginate_by = 25

class ReporterDetailView(DetailView):
    model = Reporter

# Campaign
class CampaignCRUDL(SmartCRUDL):
    model = Campaign

    class List(SmartListView):
        search_fields = ('going_on__icontains', )
        default_order = 'going_on'

# Beneficiaire
class BeneficiaireCRUDL(SmartCRUDL):
    model = Beneficiaire

    class List(SmartListView):
        search_fields = ('designation__icontains', )
        default_order = 'designation'
# Product
class ProductCRUDL(SmartCRUDL):
    model = Product

    class List(SmartListView):
        search_fields = ('name__icontains', )
        default_order = 'name'

# CampaignBeneficiary
class CampaignBeneficiaryCRUDL(SmartCRUDL):
    model = CampaignBeneficiary

    class List(SmartListView):
        search_fields = ('beneficiary__icontains', )
        default_order = 'beneficiary'

# CampaignBeneficiaryProduct
class CampaignBeneficiaryProductCRUDL(SmartCRUDL):
    model = CampaignBeneficiaryProduct

    class List(SmartListView):
        search_fields = ('campaign_beneficiary__icontains', 'campaign_product__icontains')
        default_order = 'campaign_beneficiary'

# CampaignProduct
class CampaignProductCRUDL(SmartCRUDL):
    model = CampaignProduct

    class List(SmartListView):
        search_fields = ('product__icontains', )
        default_order = 'product'

# CampaignProduct
class ReportCRUDL(SmartCRUDL):
    actions = ('read', 'list')
    model = Report

    class List(SmartListView):
        fields = ('text', 'reporting_date', 'concerned_date',  'category', 'cds', 'cds.district', 'cds.district.province')
        search_fields = ('text__icontains', 'cds__name__icontains')
        default_order = 'cds'

# ReportBeneficiary
class ReportBeneficiaryCRUDL(SmartCRUDL):
    actions = ('read', 'list')
    model = ReportBeneficiary

    class List(SmartListView):
        fields = ('campaign_beneficiary.beneficiary', 'campaign_beneficiary.campaign','report', 'report.cds', 'reception_date', 'received_number')
        search_fields = ('report__text__icontains', 'campaign_beneficiary__beneficiary__designation__icontains')
        default_order = 'report'

# ReportProductReception
class ReportProductReceptionCRUDL(SmartCRUDL):
    actions = ('read', 'list')
    model = ReportProductReception

    class List(SmartListView):
        search_fields = ('report__text__icontains', 'campaign_product__product__name__icontains')
        default_order = 'report'

# ReportProductRemainStock
class ReportProductRemainStockCRUDL(SmartCRUDL):
    actions = ('read', 'list')
    model = ReportProductRemainStock

    class List(SmartListView):
        search_fields = ('report__text__icontains', 'campaign_product__product__name__icontains')
        default_order = 'report'

# ProfileUser
class ProfileUserCRUDL(SmartCRUDL):
    actions = ('update', 'list', 'read')
    model = ProfileUser

    class List(SmartListView):
        fields = ('user', 'telephone', 'user.email', 'level', 'moh_facility')
        search_fields = ('user__name__icontains', 'telephone__icontains', 'user__email__icontains')
        default_order = 'user'

#Campaign

FORMS = [("campaign", CampaignForm1),
         ("product", CampaignForm2),
         ("beneficiary", CampaignForm3)]


class CampaignWizard(SessionWizardView):
    def done(self, form_list, form_dict, **kwargs):
        campaign = form_dict['campaign'].save()
        product = form_dict['product'].save(commit=False)
        product.campaign = campaign
        product.save()
        beneficiary = form_dict['beneficiary'].save(commit=False)
        beneficiary.campaign = campaign
        beneficiary.save()
        url = reverse('ssme_activities.campaign_list')
        return HttpResponseRedirect(url)