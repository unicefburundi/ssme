from django.shortcuts import render
from ssme_activities.models import *
from ssme_activities.forms import *
from django.views.generic import ListView, DetailView, CreateView

def dashboard(request):
    return render(request, 'base_layout.html')

def moh_facility(request):
    return render(request, 'ssme_activities/moh_facility.html')

def profile_user(request):
    return render(request, 'ssme_activities/profile_user.html')

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