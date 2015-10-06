from django.shortcuts import render
from ssme_activities.models import *
from ssme_activities.forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

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
class CampaignCreateView(CreateView):
    model = Campaign
    form_class = CampaignForm

class CampaignCDSListView(ListView):
    model = CampaignCDS
    paginate_by = 25

class CampaignDetailView(DetailView):
    model = Campaign

# Beneficiaire
class BeneficiaireCreateView(CreateView):
    model = Beneficiaire
    form_class = BeneficiaireForm

class BeneficiaireListView(ListView):
    model = Beneficiaire
    paginate_by = 25

class BeneficiaireDetailView(DetailView):
    model = Beneficiaire

# Product
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm

class ProductListView(ListView):
    model = Product
    paginate_by = 25

class ProductDetailView(DetailView):
    model = Product

# CampaignBeneficiary
class CampaignBeneficiaryCreateView(CreateView):
    model = CampaignBeneficiary
    form_class = CampaignBeneficiaryForm

class CampaignBeneficiaryListView(ListView):
    model = CampaignBeneficiary
    paginate_by = 25

class CampaignBeneficiaryDetailView(DetailView):
    model = CampaignBeneficiary

# CampaignProduct
class CampaignProductCreateView(CreateView):
    model = CampaignProduct
    form_class = CampaignProductForm

class CampaignProductListView(ListView):
    model = CampaignProduct
    paginate_by = 25

class CampaignProductDetailView(DetailView):
    model = CampaignProduct

# CampaignBeneficiaryProduct
class CampaignBeneficiaryProductCreateView(CreateView):
    model = CampaignBeneficiaryProduct
    form_class = CampaignBeneficiaryProductForm

class CampaignBeneficiaryProductListView(ListView):
    model = CampaignBeneficiaryProduct
    paginate_by = 25

class CampaignBeneficiaryProductDetailView(DetailView):
    model = CampaignBeneficiaryProduct

# Report
class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm

class ReportListView(ListView):
    model = Report
    paginate_by = 25

class ReportDetailView(DetailView):
    model = Report

# ReportBeneficiary
class ReportBeneficiaryCreateView(CreateView):
    model = ReportBeneficiary
    form_class = ReportBeneficiaryForm

class ReportBeneficiaryListView(ListView):
    model = ReportBeneficiary
    paginate_by = 25

class ReportBeneficiaryDetailView(DetailView):
    model = ReportBeneficiary

# ReportProductReception
class ReportProductReceptionCreateView(CreateView):
    model = ReportProductReception
    form_class = ReportProductReceptionForm

class ReportProductReceptionListView(ListView):
    model = ReportProductReception
    paginate_by = 25

class ReportProductReceptionDetailView(DetailView):
    model = ReportProductReception

# ReportProductRemainStock
class ReportProductRemainStockCreateView(CreateView):
    model = ReportProductRemainStock
    form_class = ReportProductRemainStockForm

class ReportProductRemainStockListView(ListView):
    model = ReportProductRemainStock
    paginate_by = 25

class ReportProductRemainStockDetailView(DetailView):
    model = ReportProductRemainStock

