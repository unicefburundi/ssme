from django.shortcuts import render
from ssme_activities.models import *
from ssme_activities.forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from smartmin.views import *
from formtools.wizard.views import SessionWizardView
from ssme.context_processor import myfacility, get_per_category_taux
from ssme_activities.tables import *
from django.contrib.auth.forms import PasswordResetForm
from django.db.models import F, Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

today = {'reception_date': datetime.date.today().strftime('%Y-%m-%d')}

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

def get_pop_total(request, code=''):
    pop_total = CampaignCDS.objects.all()
    if  not code :
        return pop_total.values('population_cible').aggregate(population_cible=Sum('population_cible'))
    if not pop_total:
        pop_total= {}
        pop_total['population_cible'] = 0
    elif len(code)<=2 :
        return pop_total.filter(cds__district__province__code=int(code)).values('population_cible').aggregate(population_cible=Sum('population_cible'))
    if len(code)>2 and len(code)<=4 :
        return pop_total.filter(cds__district__code=int(code)).values('population_cible').aggregate(population_cible=Sum('population_cible'))
    if len(code)>4 :
        return pop_total.filter(cds__code=int(code)).values('population_cible').aggregate(population_cible=Sum('population_cible'))

def get_report_by_code(request, code, model):
    queryset = model.objects.all()
    if not queryset :
        return queryset
    if not code :
        return queryset
    if len(code)<=2 :
        return queryset.filter(report__cds__district__province__code=int(code))
    if len(code)>2 and len(code)<=4 :
        return queryset.filter(report__cds__district__code=int(code))
    if len(code)>4 :
        return queryset.filter(report__cds__code=code)


def get_benef(queryset_benef, dates_benef, headers_benef, **kwargs ):
    body_benef = {}
    if not dates_benef:
        res, ress = today, {}
        if 'cds' in kwargs :
            queryset_benef = queryset_benef.filter( report__cds=kwargs.get('cds').id)
            if not queryset_benef :
                return []
            else:
                for t in headers_benef:
                    ress =  queryset_benef.annotate(beneficiaires=F('campaign_beneficiary__beneficiary__designation')).filter(reception_date__lte=today['reception_date'], beneficiaires=t['beneficiaires']).values('received_number')
                    if not ress:
                        res.update({t['beneficiaires']:0})
                    else:
                        ress = reduce(lambda x, y: dict((k, v + y[k]) for k, v in x.iteritems()), ress)
                        res.update({t['beneficiaires']:ress['received_number']})
                    body_benef.update(res)
                return body_benef
        elif 'district' in kwargs:
            queryset_benef = queryset_benef.filter( report__cds__district=kwargs.get('district').id)
        elif 'province' in kwargs:
            queryset_benef = queryset_benef.filter( report__cds__district__province=kwargs.get('province').id)
        if not queryset_benef :
            return []
        else:
            for t in headers_benef:
                ress =  queryset_benef.annotate(beneficiaires=F('campaign_beneficiary__beneficiary__designation')).filter(reception_date__lte=today['reception_date'], beneficiaires=t['beneficiaires']).values('received_number')
                if not ress:
                    res.update({t['beneficiaires']:0})
                else:
                    ress = reduce(lambda x, y: dict((k, v + y[k]) for k, v in x.iteritems()), ress)
                    res.update({t['beneficiaires']:ress['received_number']})
                body_benef.update(res)
            return body_benef
    else:
        body_benef = []
        for i in dates_benef:
            res, ress = i, {}
            for t in headers_benef:
                ress =  queryset_benef.annotate(beneficiaires=F('campaign_beneficiary__beneficiary__designation')).filter(reception_date=i['reception_date'], beneficiaires=t['beneficiaires']).values('received_number').aggregate(total=Sum('received_number'))
                if not ress['total']:
                    res.update({t['beneficiaires']:0})
                else:
                    res.update({t['beneficiaires']:ress['total']})
            body_benef.append(res)
        return body_benef

def get_reception(queryset_reception, dates_reception, headers_recept, **kwargs):
    body_reception = {}
    if not dates_reception:
        res, ress = today, {}
        if 'cds' in kwargs :
            queryset_reception = queryset_reception.filter( report__cds=kwargs.get('cds').id)
        elif 'district' in kwargs:
            queryset_reception = queryset_reception.filter( report__cds__district=kwargs.get('district').id)
        elif 'province' in kwargs:
            queryset_reception = queryset_reception.filter( report__cds__district__province=kwargs.get('province').id)
        if not queryset_reception :
            return []
        else:
            for t in headers_recept:
                ress =  queryset_reception.annotate(products=F('campaign_product__product__name')).filter(reception_date__lte=today['reception_date'], products=t['products']).values('received_quantity').aggregate(total=Sum('received_quantity'))
                if not ress['total']:
                    res.update({t['products']:0})
                else:
                    res.update({t['products']:ress['total']})
            body_reception.update(res)
        return body_reception
    else:
        body_reception = []
        for i in dates_reception:
            res, ress = i, {}
            for t in headers_recept:
                ress =  queryset_reception.annotate(products=F('campaign_product__product__name')).filter(reception_date=i['reception_date'], products=t['products']).values('received_quantity').aggregate(total=Sum('received_quantity'))
                if not ress['total'] :
                    res.update({t['products']:0})
                else:
                    res.update({t['products']:ress['total']})
            body_reception.append(res)
        return body_reception

def get_remain(queryset_remain, dates_remain, headers_recept, **kwargs):
    body_remain = {}
    if not dates_remain:
        res, ress = today, {}
        if 'cds' in kwargs :
            queryset_remain = queryset_remain.filter( report__cds=kwargs.get('cds').id)
        elif 'district' in kwargs:
            queryset_remain = queryset_remain.filter( report__cds__district=kwargs.get('district').id)
        elif 'province' in kwargs:
            queryset_remain = queryset_remain.filter( report__cds__district__province=kwargs.get('province').id)
        if not queryset_remain :
            return []
        else:
            for t in headers_recept:
                ress =  queryset_remain.annotate(products=F('campaign_product__product__name')).filter(concerned_date__lte=today['reception_date'], products=t['products']).values('remain_quantity').aggregate(total=Sum('remain_quantity'))
                if not ress['total']:
                    res.update({t['products']:0})
                else:
                    res.update({t['products']:ress['total']})
            body_remain.update(res)
        return body_remain
    else:
        body_remain = []
        for i in dates_remain:
            res, ress = i, {}
            for t in headers_recept:
                ress =  queryset_remain.annotate(products=F('campaign_product__product__name')).filter(concerned_date=i['concerned_date'], products=t['products']).values('remain_quantity').aggregate(total=Sum('remain_quantity'))
                if not ress['total'] :
                    res.update({t['products']:0})
                else:
                    res.update({t['products']:ress['total']})
            body_remain.append(res)
        return body_remain

#Province
class ProvinceCreateView(CreateView):
    model = Province
    form_class = ProvinceForm

class ProvinceListView(ListView):
    model = Province
    paginate_by = 100

class ProvinceDetailView(DetailView):
    model = Province

    def get_context_data(self, **kwargs):
        context = super(ProvinceDetailView, self).get_context_data(**kwargs)
        mycode = str(context['object'].code)
        districts = District.objects.filter(province__code=mycode)
        pop_total = CampaignCDS.objects.filter(cds__district__province__code=mycode)
        if not pop_total:
            pop_total= {}
            pop_total['population_cible'] = 0
        else:
            pop_total = pop_total.values('population_cible').aggregate(population_cible=Sum('population_cible'))
        context['pop_total'] = pop_total
        #benef
        #benef
        headers_benef = CampaignBeneficiary.objects.filter(campaign__going_on=True).annotate(beneficiaires=F('beneficiary__designation')).values('beneficiaires').distinct().order_by("id")
        queryset_benef = get_report_by_code(self.request, mycode, ReportBeneficiary)
        dates_today = []
        body_benef = []
        for district in districts :
            res = get_benef(queryset_benef, dates_today, headers_benef, district=district)
            if  res == []:
                pass
            else :
                res.update({'district':district})
                body_benef.append(res)
        context['body_benef'] = body_benef
        context['headers_benef'] = headers_benef
        #reception
        headers_recept = CampaignProduct.objects.filter(campaign__going_on=True).annotate(products=F('product__name')).values('products').distinct()
        queryset_reception = get_report_by_code(self.request, mycode, ReportProductReception)
        body_reception = []
        for district in districts :
            res = get_reception(queryset_reception, dates_today, headers_recept, district=district)
            if  res == []:
                pass
            else :
                res.update({'district':district})
                body_reception.append(res)
        context['body_reception'] = body_reception
        context['headers_recept'] = headers_recept

        # Remain
        queryset_remain = get_report_by_code(self.request, mycode, ReportProductRemainStock)
        body_remain = []
        for district in districts :
            res = get_remain(queryset_remain, dates_today, headers_recept, district=district)
            if  res == []:
                pass
            else :
                res.update({'district':district})
                body_remain.append(res)
        context['body_remain'] = body_remain
        context['taux'] = get_per_category_taux(self.request)
        return context

# District
class DistrictCreateView(CreateView):
    model = District
    form_class = DistrictForm

class DistrictListView(ListView):
    model = District
    paginate_by = 100

class DistrictDetailView(DetailView):
    model = District

    def get_context_data(self, **kwargs):
        context = super(DistrictDetailView, self).get_context_data(**kwargs)
        mycode = str(context['object'].code)
        cdss = CDS.objects.filter(district__code=mycode)
        pop_total = CampaignCDS.objects.filter(cds__district__code=mycode)
        if not pop_total:
            pop_total= {}
            pop_total['population_cible'] = 0
        else:
            pop_total = pop_total.values('population_cible').aggregate(population_cible=Sum('population_cible'))
        context['pop_total'] = pop_total
        #benef
        headers_benef = CampaignBeneficiary.objects.filter(campaign__going_on=True).annotate(beneficiaires=F('beneficiary__designation')).values('beneficiaires').distinct().order_by("id")
        queryset_benef = get_report_by_code(self.request, mycode, ReportBeneficiary)
        dates_today = []
        body_benef = []
        for cds in cdss :
            res = get_benef(queryset_benef, dates_today, headers_benef, cds=cds)
            if  res == []:
                pass
            else :
                res.update({'cds':cds})
                body_benef.append(res)
        context['body_benef'] = body_benef
        context['headers_benef'] = headers_benef
        #reception
        headers_recept = CampaignProduct.objects.filter(campaign__going_on=True).annotate(products=F('product__name')).values('products').distinct()
        queryset_reception = get_report_by_code(self.request, mycode, ReportProductReception)
        body_reception = []
        for cds in cdss :
            res = get_reception(queryset_reception, dates_today, headers_recept, cds=cds)
            if  res == []:
                pass
            else :
                res.update({'cds':cds})
                body_reception.append(res)
        context['body_reception'] = body_reception
        context['headers_recept'] = headers_recept

        # Remain
        queryset_remain = get_report_by_code(self.request, mycode, ReportProductRemainStock)
        body_remain = []
        for cds in cdss :
            res = get_remain(queryset_remain, dates_today, headers_recept, cds=cds)
            if  res == []:
                pass
            else :
                res.update({'cds':cds})
                body_remain.append(res)
        context['body_remain'] = body_remain
        context['taux'] = get_per_category_taux(self.request)
        return context

# CDS
class CDSCreateView(CreateView):
    model = CDS
    form_class = CDSForm

class CDSListView(ListView):
    model = CDS
    paginate_by = 1000

class CDSDetailView(DetailView):
    model = CDS

    def get_context_data(self, **kwargs):
        context = super(CDSDetailView, self).get_context_data(**kwargs)
        mycode = str(context['object'].code)
        pop_total = CampaignCDS.objects.filter(cds__code=mycode)
        if not pop_total:
            pop_total= {}
            pop_total['population_cible'] = 0
        else:
            pop_total = pop_total.latest('id')
        # beneficiaires
        headers_benef = CampaignBeneficiary.objects.filter(campaign__going_on=True).annotate(beneficiaires=F('beneficiary__designation')).values('beneficiaires').distinct().order_by("id")
        queryset_benef = get_report_by_code(self.request, mycode, ReportBeneficiary)
        dates_benef = queryset_benef.values('reception_date').distinct().order_by('reception_date')
        body_benef = []
        if queryset_benef:
            body_benef = get_benef(queryset_benef, dates_benef, headers_benef)
        #reception
        headers_recept = CampaignProduct.objects.filter(campaign__going_on=True).annotate(products=F('product__name')).values('products').distinct()
        queryset_reception = get_report_by_code(self.request, mycode, ReportProductReception)
        dates_reception = queryset_reception.values('reception_date').distinct().order_by('reception_date')
        body_reception = []
        if queryset_reception:
            body_reception = get_reception(queryset_reception, dates_reception, headers_recept)
        # Remain
        queryset_remain = get_report_by_code(self.request, mycode, ReportProductRemainStock)
        dates_remain = queryset_remain.values('concerned_date').distinct().order_by('concerned_date')
        body_remain  = []
        if queryset_remain:
            body_remain = get_remain(queryset_remain, dates_remain, headers_recept)
        context['body_benef'] = body_benef
        context['body_reception'] = body_reception
        context['body_remain'] = body_remain
        context['headers_recept'] = headers_recept
        context['headers_benef'] = headers_benef
        context['pop_total'] = pop_total
        context['taux'] = get_per_category_taux(self.request)
        return context

# ProfileUser
class UserSignupView(CreateView):
    form_class = UserCreationMultiForm
    template_name = 'registration/create_profile.html'

    def get_success_url(self, user):
        return reverse( 'profile_user_detail', kwargs = {'pk': user})

    def form_valid(self, form):
        # Save the user first, because the profile needs a user before it
        # can be saved.
        user = form['user'].save()
        profile = form['profile'].save(commit=False)
        group = Group.objects.get_or_create(name=form['profile'].cleaned_data['level'])
        user.groups.add(group[0])
        profile.user = user
        profile.save()
        if form['user'].cleaned_data['password1'] == '' or form['user'].cleaned_data['password2'] == '':
            try:
                reset_form = PasswordResetForm({'email': user.email})
                assert reset_form.is_valid()
                reset_form.save(
                    request=self.request,
                    use_https=self.request.is_secure(),
                    subject_template_name='registration/account_creation_subject.txt',
                    email_template_name='registration/account_creation_email.html',
                )
                messages.success(self.request, 'Prifile created and mail sent to {0}.'.format(user.email))
            except:
                messages.success(self.request, 'Unable to send mail  to {0}.'.format(user.email))
                pass
        return redirect(self.get_success_url(profile.id))

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
    actions = ('read', 'list', 'create', 'update', 'delete')
    model = Campaign
    permissions = False

    class List(SmartListView):
        search_fields = ('going_on__icontains', )
        default_order = 'going_on'

    class Create(SmartCreateView):
        form_class = CampaignForm1

        def form_valid(self, form):
            messages.success(self.request, 'Campaign created {0} .'.format(form.cleaned_data['name']))
            return super(SmartCreateView, self).form_valid(form)

        def post(self, request, *args, **kwargs):
            """
            Handles POST requests, instantiating a form instance with the passed
            POST variables and then checked for validity.
            """
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            if form.is_valid():
                self.form_valid(form)
                url = reverse('ssme_activities.campaignbeneficiary_create')
                return HttpResponseRedirect(url)
            else:
                return self.form_invalid(form)



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

# CampaignCDS
class CampaignCDSCRUDL(SmartCRUDL):
    actions = ('read', 'list')
    model = CampaignCDS

    class List(SmartListView):
        fields = ('cds', 'population_cible', 'cds.district.name', 'cds.district.province.name')
        search_fields = ('cds__name__icontains', 'cds__district__name__icontains', 'cds__district__province__name__icontains')
        default_order = 'cds'

    class Export( SmartXlsView):
        pass

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

FORMS = [("campaign", CampaignForm1),
         ("product", ProductsFormSet),
         ("beneficiary", BeneficiaryFormSet),
         ]


class CampaignWizard(SessionWizardView):
    def done(self, form_list, form_dict, **kwargs):
        campaign = form_dict['campaign'].save()
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

        return HttpResponseRedirect(campaign.get_absolute_url())


@login_required
def get_reports(request, **kwargs):
    mycode = myfacility(request)
    if  'cds' in kwargs:
        mycode['mycode'] = kwargs.get('cds').code
    if not mycode['mycode'] and not request.user.groups.filter(name='CEN').exists() and not request.user.is_superuser:
        messages.warning(request, 'You have no valid MoH facility attached to your profile. Please contact the Admin')
        url = reverse('profile_user_detail', kwargs={'pk': mycode['myprofile'].id})
        return HttpResponseRedirect(url)

    # pop total
    pop_total = get_pop_total(request, mycode['mycode'])

    # beneficiaires
    headers_benef = CampaignBeneficiary.objects.filter(campaign__going_on=True).annotate(beneficiaires=F('beneficiary__designation')).values('beneficiaires').distinct().order_by("id")
    queryset_benef = get_report_by_code(request, mycode['mycode'], ReportBeneficiary)
    dates_benef = []
    body_benef = []
    if not queryset_benef:
        pass
    else:
        dates_benef = queryset_benef.values('reception_date').distinct().order_by('reception_date')
        body_benef = get_benef(queryset_benef, dates_benef, headers_benef)
    #reception
    headers_recept = CampaignProduct.objects.filter(campaign__going_on=True).annotate(products=F('product__name')).values('products').distinct()
    queryset_reception = get_report_by_code(request, mycode['mycode'], ReportProductReception)
    dates_reception = []
    body_reception = []
    if not queryset_reception:
        pass
    else:
        dates_reception = queryset_reception.values('reception_date').distinct().order_by('reception_date')
        body_reception = get_reception(queryset_reception, dates_reception, headers_recept)

    # Remain
    queryset_remain = get_report_by_code(request, mycode['mycode'], ReportProductRemainStock)
    dates_remain = []
    body_remain = []
    if not queryset_remain:
        pass
    else:
        dates_remain = queryset_remain.values('concerned_date').distinct().order_by('concerned_date')
        body_remain = get_remain(queryset_remain, dates_remain, headers_recept)
    taux = get_per_category_taux(request)

    return  render(request, "ssme_activities/reports.html", {'body_benef':body_benef, 'headers_benef': headers_benef, 'headers_recept':headers_recept, 'body_reception': body_reception, 'body_remain': body_remain, 'pop_total' : pop_total, 'taux':taux})

# Central
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def get_reports_json(request):
    data = json.dumps([dict(item) for item in ReportBeneficiary.objects.annotate(beneficiaires=F('campaign_beneficiary__beneficiary__designation')).values('beneficiaires',  'reception_date','received_number')], default=date_handler)

    return HttpResponse(data, content_type='application/json')