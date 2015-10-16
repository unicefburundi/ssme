from django.shortcuts import render
from ssme_activities.models import *
from ssme_activities.forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from smartmin.views import *
from formtools.wizard.views import SessionWizardView
from ssme.context_processor import myfacility
from django_tables2   import RequestConfig
from ssme_activities.tables import *
from django.contrib.auth.forms import PasswordResetForm
from django.db.models import F
from django.contrib.auth.decorators import login_required


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

def get_report_by_code(request, code, model):
    queryset = model.objects.all()
    if not code and request.user.groups.filter(name='Central') :
        return queryset
    if len(code)<=2 :
        return queryset.filter(report__cds__district__province__code=int(code))
    if len(code)>2 and len(code)<=4 :
        return queryset.filter(report__cds__district__code=int(code))
    if len(code)>4 :
        return queryset.filter(report__cds__code=code)

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
        # import ipdb; ipdb.set_trace()
        if form['user'].cleaned_data['password1'] == '' or form['user'].cleaned_data['password2'] == '':
            reset_form = PasswordResetForm({'email': user.email})
            assert reset_form.is_valid()
            reset_form.save(
                request=self.request,
                use_https=self.request.is_secure(),
                subject_template_name='registration/account_creation_subject.txt',
                email_template_name='registration/account_creation_email.html',
            )
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
    actions = ('read', 'list')
    model = Campaign
    permissions = False

    class List(SmartListView):
        # import ipdb; ipdb.set_trace()
        search_fields = ('going_on__icontains', )
        default_order = 'going_on'

        def derive_queryset(self, *args, **kwargs):
            queryset = super(CampaignCRUDL.List, self).derive_queryset(*args, **kwargs)
            # import ipdb; ipdb.set_trace()
            myfacilities =  myfacility(self.request)
            if myfacilities['mycode'] == None :
                return queryset
            # elif len(str(myfacilities['mycode'])) >=5 :
            #     return queryset.filter(cds__code=myfacilities['mycode'])
            # elif 3 <= len(str(myfacilities['mycode'])) <=4 :
            #     return queryset.filter(cds__district__code=myfacilities['mycode'])
            # elif 1 <= len(str(myfacilities['mycode'])) <= 2 :
            #     return queryset.filter(cds__district__province__code=myfacilities['mycode'])
            else:
                return Campaign.objects.none()


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

    class Create(SmartCreateView):
        form_class = ProductForm

# CampaignBeneficiary
class CampaignBeneficiaryCRUDL(SmartCRUDL):
    actions = ('read', 'list')
    model = CampaignBeneficiary

    class List(SmartListView):
        search_fields = ('beneficiary__icontains', )
        default_order = 'beneficiary'

# CampaignBeneficiaryProduct
class CampaignBeneficiaryProductCRUDL(SmartCRUDL):
    actions = ('read', 'list')
    model = CampaignBeneficiaryProduct

    class List(SmartListView):
        search_fields = ('campaign_beneficiary__icontains', 'campaign_product__icontains')
        default_order = 'campaign_beneficiary'

# CampaignProduct
class CampaignProductCRUDL(SmartCRUDL):
    actions = ('read', 'list')
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

# ProfileUser
class ProfileUserCRUDL(SmartCRUDL):
    actions = ('update', 'list', 'read', 'delete')
    model = ProfileUser

    class List(SmartListView):
        fields = ('user', 'telephone', 'user.email', 'level', 'moh_facility')
        search_fields = ('user__name__icontains', 'telephone__icontains', 'user__email__icontains')
        default_order = 'user'

#Campaign

# class CDSCampaignFormSet1(CDSCampaignFormSet):
#     cds =


FORMS = [("campaign", CampaignForm1),
         ("product", ProductsFormSet),
         ("beneficiary", BeneficiaryFormSet),
         # ("cds", CDSCampaignFormSet)
         ]


class CampaignWizard(SessionWizardView):
    def done(self, form_list, form_dict, **kwargs):
        campaign = form_dict['campaign'].save()
        # import ipdb; ipdb.set_trace()
        products, orders = set(), set()
        for i in form_dict['product'].cleaned_data:
            if (i != {}) and (i['product'] not in products) and (i['order_in_sms'] not in orders):
                CampaignProduct.objects.get_or_create(campaign=campaign, product= i['product'], order_in_sms=i['order_in_sms'] )
                products.add(i['product'])
                orders.add(i['order_in_sms'])

        beneficiaries, orders = set(), set()
        for i in form_dict['beneficiary'].cleaned_data:
            if (i != {}) and (i['beneficiary'] not in beneficiaries) and (i['order_in_sms'] not in orders):
                CampaignBeneficiary.objects.get_or_create(campaign=campaign, beneficiary= i['beneficiary'], order_in_sms=i['order_in_sms'] )
                beneficiaries.add(i['beneficiary'])
                orders.add(i['order_in_sms'])

        # cdss, orders = set(), set()
        # for i in form_dict['cds'].cleaned_data:
        #     if (i != {}) and (i['cds'] not in cdss):
        #         CampaignBeneficiaryCDS.objects.get_or_create(campaign=campaign, cds= i['cds'], population_attendu=i['population_attendu'], )
        #         cdss.add(i['beneficiary'])
        #         orders.add(i['order_in_sms'])

        return HttpResponseRedirect(campaign.get_absolute_url())

@login_required
def get_reports(request):
    mycode = myfacility(request)
    report_benef = ReportBeneficiaryTable(get_report_by_code(request, mycode['mycode'], ReportBeneficiary))
    RequestConfig(request).configure(report_benef)
    report_remain = ReportProductRemainStockTable(get_report_by_code(request, mycode['mycode'],ReportProductRemainStock))
    RequestConfig(request).configure(report_remain)
    report_reception = ReportProductReceptionTable(get_report_by_code(request, mycode['mycode'],ReportProductReception))
    RequestConfig(request).configure(report_reception)

    return render(request, "ssme_activities/reports.html", {'report_benef': report_benef, 'report_remain': report_remain, 'report_reception' : report_reception })

@login_required
def get_reports2(request):
    mycode = myfacility(request)
    headers = CampaignBeneficiary.objects.filter(campaign__going_on=True).annotate(beneficiaires=F('beneficiary__designation')).values('beneficiaires').distinct()
    mycode = myfacility(request)
    queryset_benef = get_report_by_code(request, mycode['mycode'], ReportBeneficiary)
    dates_benef = ReportBeneficiary.objects.values('reception_date').distinct()
    body = []
    for i in dates_benef:
        # import ipdb; ipdb.set_trace()
        res, ress = i, {}
        for t in headers:
            # import ipdb; ipdb.set_trace()
            ress =  queryset_benef.annotate(beneficiaires=F('campaign_beneficiary__beneficiary__designation')).filter(reception_date=i['reception_date'], beneficiaires=t['beneficiaires']).values('received_number')
            if not ress:
                res.update({t['beneficiaires']:0})
            else:
                # import ipdb; ipdb.set_trace()
                res.update({t['beneficiaires']:ress[0]['received_number']})
        body.append(res)
    report_remain = ReportProductRemainStockTable(get_report_by_code(request, mycode['mycode'],ReportProductRemainStock))
    RequestConfig(request).configure(report_remain)
    report_reception = ReportProductReceptionTable(get_report_by_code(request, mycode['mycode'],ReportProductReception))
    RequestConfig(request).configure(report_reception)

    return  render(request, "ssme_activities/reports.html", {'body':body, 'headers': headers, 'report_remain': report_remain, 'report_reception' : report_reception })

