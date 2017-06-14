import datetime
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.db.models import F, Sum
from django.utils.translation import ugettext as _
from formtools.wizard.views import SessionWizardView
from ssme.context_processor import *
from ssme_activities.models import *
from ssme_activities.forms import *
from ssme_activities.tables import *
from smartmin.views import *
import json
from django.db.models import Sum
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum
from ssme_activities.serilaizers import *
from rest_framework import viewsets

today = {'reception_date': datetime.date.today().strftime('%Y-%m-%d')}


def dashboard(request):
    d = {}
    d['campaigns'] = Campaign.objects.all()
    return render(request, 'base_layout.html', d)


def moh_facility(request):
    cds_form = CDSForm
    district_form = DistrictForm
    province_form = ProvinceForm
    return render(request, 'ssme_activities/moh_facility.html', {'cds_form':cds_form, 'district_form':district_form, 'province_form':province_form})


def profile_user(request):
    profile_form = UserCreationMultiForm
    return render(request, 'ssme_activities/profile_user.html', {'profile_form': profile_form})


def campaigns(request):
    return render(request, 'ssme_activities/campaigns.html')


def beneficiaries(request):
    return render(request, 'ssme_activities/beneficiaries.html')


def get_pop_total(request, code=''):
    pop_total = CampaignCDS.objects.all()
    if not code:
        return pop_total.values('population_cible').aggregate(population_cible=Sum('population_cible'))
    if not pop_total:
        pop_total = {}
        pop_total['population_cible'] = 0
    elif len(code) <=2:
        return pop_total.filter(cds__district__province__code=int(code)).values('population_cible').aggregate(population_cible=Sum('population_cible'))
    if len(code) > 2 and len(code) <= 4:
        return pop_total.filter(cds__district__code=int(code)).values('population_cible').aggregate(population_cible=Sum('population_cible'))
    if len(code) > 4:
        return pop_total.filter(cds__code=int(code)).values('population_cible').aggregate(population_cible=Sum('population_cible'))


def get_report_by_code(request, code, model):
    queryset = model.objects.all()
    if not queryset:
        return queryset
    if not code:
        return queryset
    if len(code) <= 2:
        return queryset.filter(report__cds__district__province__code=int(code))
    if len(code) > 2 and len(code) <= 4:
        return queryset.filter(report__cds__district__code=int(code))
    if len(code) > 4:
        return queryset.filter(report__cds__code=code)


def get_benef(queryset_benef, dates_benef, headers_benef, **kwargs ):
    body_benef = {}
    if not dates_benef:
        res, ress = today, {}
        if 'cds' in kwargs:
            queryset_benef = queryset_benef.filter(report__cds=kwargs.get('cds').id)
            if not queryset_benef:
                return []
            else:
                for t in headers_benef:
                    ress = queryset_benef.annotate(beneficiaires=F('campaign_beneficiary__beneficiary__designation')).filter(reception_date__lte=today['reception_date'], beneficiaires=t['beneficiaires']).values('received_number')
                    if not ress:
                        res.update({t['beneficiaires']:0})
                    else:
                        ress = reduce(lambda x, y: dict((k, v + y[k]) for k, v in x.iteritems()), ress)
                        res.update({t['beneficiaires']:ress['received_number']})
                    body_benef.update(res)
                return body_benef
        elif 'district' in kwargs:
            queryset_benef = queryset_benef.filter(report__cds__district=kwargs.get('district').id)
        elif 'province' in kwargs:
            queryset_benef = queryset_benef.filter(report__cds__district__province=kwargs.get('province').id)
        if not queryset_benef:
            return []
        else:
            for t in headers_benef:
                ress = queryset_benef.annotate(beneficiaires=F('campaign_beneficiary__beneficiary__designation')).filter(reception_date__lte=today['reception_date'], beneficiaires=t['beneficiaires']).values('received_number')
                if not ress:
                    res.update({t['beneficiaires']: 0})
                else:
                    ress = reduce(lambda x, y: dict((k, v + y[k]) for k, v in x.iteritems()), ress)
                    res.update({t['beneficiaires']: ress['received_number']})
                body_benef.update(res)
            return body_benef
    else:
        body_benef = []
        for i in dates_benef:
            res, ress = i, {}
            for t in headers_benef:
                ress = queryset_benef.annotate(beneficiaires=F('campaign_beneficiary__beneficiary__designation')).filter(reception_date=i['reception_date'], beneficiaires=t['beneficiaires']).values('received_number').aggregate(total=Sum('received_number'))
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
        if 'cds' in kwargs:
            queryset_reception = queryset_reception.filter( report__cds=kwargs.get('cds').id)
        elif 'district' in kwargs:
            queryset_reception = queryset_reception.filter( report__cds__district=kwargs.get('district').id)
        elif 'province' in kwargs:
            queryset_reception = queryset_reception.filter( report__cds__district__province=kwargs.get('province').id)
        if not queryset_reception:
            return []
        else:
            for t in headers_recept:
                ress =  queryset_reception.annotate(products=F('campaign_product__product__name')).filter(reception_date__lte=today['reception_date'], products=t['products']).values('received_quantity').aggregate(total=Sum('received_quantity'))
                if not ress['total']:
                    res.update({t['products']: 0})
                else:
                    res.update({t['products']: ress['total']})
            body_reception.update(res)
        return body_reception
    else:
        body_reception = []
        for i in dates_reception:
            res, ress = i, {}
            for t in headers_recept:
                ress = queryset_reception.annotate(products=F('campaign_product__product__name')).filter(reception_date=i['reception_date'], products=t['products']).values('received_quantity').aggregate(total=Sum('received_quantity'))
                if not ress['total']:
                    res.update({t['products']: 0})
                else:
                    res.update({t['products']: ress['total']})
            body_reception.append(res)
        return body_reception


def get_remain_cds(queryset_remain, dates_remain, headers_recept, **kwargs):
    if not dates_remain:
        body_remain, rest, ress = {}, {}, {}
        cds = CDS.objects.get(pk=kwargs.get('cds'))

        for t in headers_recept:
            ress = queryset_remain.annotate(products=F('campaign_product__product__name')).filter(products=t['products'])
            if not ress:
                rest.update({str(t['products']): 0})
            else:
                ress = ress.values('remain_quantity').latest('concerned_date')
                rest.update({str(t['products']): ress['remain_quantity']})
        body_remain.update(rest)
        body_remain.update({'cds': cds})
        return body_remain
    else:
        body_remain, rest, ress = {}, {}, {}
        for t in headers_recept:
            ress = queryset_remain.annotate(products=F('campaign_product__product__name')).filter(products=t['products']).values('remain_quantity').aggregate(total=Sum('remain_quantity'))
            if not ress['total']:
                rest.update({str(t['products']): 0})
            else:
                rest.update({str(t['products']): ress['total']})
        body_remain.update(rest)
        return body_remain


def get_remain(queryset_remain, dates_remain, headers_recept, **kwargs):
    if not dates_remain:
        if 'cds' in kwargs:
            queryset_remain = queryset_remain.filter(report__cds=kwargs.get('cds'))
            cds_r = get_remain_cds(queryset_remain, dates_remain, headers_recept, cds=kwargs.get('cds'))
            return cds_r
        elif 'district' in kwargs:
            district_r = []
            queryset_remain = queryset_remain.filter(report__cds__district=kwargs.get('district'))
            for i in queryset_remain.values('report__cds').distinct():
                district_r.append(get_remain(queryset_remain, dates_remain, headers_recept, cds=i['report__cds']))
            return district_r

        elif 'province' in kwargs:
            province_r = []
            queryset_remain = queryset_remain.filter(report__cds__district__province=kwargs.get('province').id)
            for i in queryset_remain.values('report__cds__district').distinct():
                district = District.objects.get(pk=i['report__cds__district'])
                somme = get_remain(queryset_remain, dates_remain, headers_recept, district=district)
                for i in somme:
                    del i['cds']
                somme = add_elements_in_dict(somme)
                somme.update({'district': district})
                province_r.append(somme)
            return province_r
        if not queryset_remain:
            return []
    else:
        body_remain = []
        for d in dates_remain:
            queryset = queryset_remain.filter(concerned_date__lte=d['concerned_date'])
            bb = []
            for i in queryset.values('report__cds').distinct():
                queryset_temp = queryset.filter(report__cds=i['report__cds'])
                if queryset_temp:
                    bb.append(get_remain_cds(queryset_temp, [], headers_recept, cds=i['report__cds']))
            for i in bb:
                del i['cds']
            bb = add_elements_in_dict(bb)
            bb.update(d)
            body_remain.append(bb)
        return body_remain


# Province
class ProvinceCreateView(CreateView):
    model = Province
    form_class = ProvinceForm


class ProvinceListView(ListView):
    model = Province
    paginate_by = 100

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProvinceListView, self).dispatch(*args, **kwargs)
        
    def get_queryset(self):
        """Returns Province that belong to the current user"""
        mycode = myfacility(self.request)
        if not mycode['mycode']:
            return Province.objects.all()
        else:
            return Province.objects.filter(code=mycode['mycode'])


class ProvinceDetailView(DetailView):
    model = Province
    lookup_field = 'code'

    def get_context_data(self, **kwargs):
        context = super(ProvinceDetailView, self).get_context_data(**kwargs)
        mycode = str(context['object'].code)
        districts = District.objects.filter(province__code=mycode)
        pop_total = CampaignCDS.objects.filter(cds__district__province__code=mycode)
        if not pop_total:
            pop_total = {}
            pop_total['population_cible'] = 0
        else:
            pop_total = pop_total.values('population_cible').aggregate(population_cible=Sum('population_cible'))
        context['pop_total'] = pop_total
        # benef
        headers_benef = CampaignBeneficiary.objects.all().annotate(beneficiaires=F('beneficiary__designation')).values('beneficiaires').distinct().order_by("id")
        queryset_benef = get_report_by_code(self.request, mycode, ReportBeneficiary)
        dates_today = []
        body_benef = []
        for district in districts:
            res = get_benef(queryset_benef, dates_today, headers_benef, district=district)
            if res == []:
                pass
            else:
                res.update({'district': district})
                body_benef.append(res)
        context['body_benef'] = body_benef
        context['headers_benef'] = headers_benef
        # reception
        headers_recept = CampaignProduct.objects.all().annotate(products=F('product__name')).values('products').distinct().order_by('order_in_sms')
        queryset_reception = get_report_by_code(self.request, mycode, ReportProductReception)
        body_reception = []
        for district in districts:
            res = get_reception(queryset_reception, dates_today, headers_recept, district=district)
            if res == []:
                pass
            else:
                res.update({'district': district})
                body_reception.append(res)
        context['body_reception'] = body_reception
        context['headers_recept'] = headers_recept

        # Remain
        queryset_remain = get_report_by_code(self.request, mycode, ReportProductRemainStock)
        body_remain = get_remain(queryset_remain, dates_today, headers_recept, province=context['object'])
        context['body_remain'] = body_remain
        context['taux'] = get_per_category_taux(self.request)
        context['recus'] = total_received(self.request, mycode)
        return context


# District
class DistrictCreateView(CreateView):
    model = District
    form_class = DistrictForm


class DistrictListView(ListView):
    model = District
    paginate_by = 100

    def get_queryset(self):
        """Returns Province that belong to the current user"""
        mycode = myfacility(self.request)
        if not mycode['mycode']:
            return District.objects.all()
        else:
            if len(mycode['mycode']) < 3:
                return District.objects.filter(province__code=mycode['mycode'])
            else:
                return District.objects.filter(code=mycode['mycode'])


class DistrictDetailView(DetailView):
    model = District
    lookup_field = 'code'

    def get_context_data(self, **kwargs):
        context = super(DistrictDetailView, self).get_context_data(**kwargs)
        mycode = str(context['object'].code)
        cdss = CDS.objects.filter(district__code=mycode)
        pop_total = CampaignCDS.objects.filter(cds__district__code=mycode)
        if not pop_total:
            pop_total = {}
            pop_total['population_cible'] = 0
        else:
            pop_total = pop_total.values('population_cible').aggregate(population_cible=Sum('population_cible'))
        context['pop_total'] = pop_total
        # benef
        headers_benef = CampaignBeneficiary.objects.all().annotate(beneficiaires=F('beneficiary__designation')).values('beneficiaires').distinct().order_by("id")
        queryset_benef = get_report_by_code(self.request, mycode, ReportBeneficiary)
        dates_today = []
        body_benef = []
        for cds in cdss:
            res = get_benef(queryset_benef, dates_today, headers_benef, cds=cds)
            if res == []:
                pass
            else:
                res.update({'cds': cds})
                body_benef.append(res)
        context['body_benef'] = body_benef
        context['headers_benef'] = headers_benef
        # reception
        headers_recept = CampaignProduct.objects.all().annotate(products=F('product__name')).values('products').distinct().order_by('order_in_sms')
        queryset_reception = get_report_by_code(self.request, mycode, ReportProductReception)
        body_reception = []
        for cds in cdss:
            res = get_reception(queryset_reception, dates_today, headers_recept, cds=cds)
            if res == []:
                pass
            else:
                res.update({'cds': cds})
                body_reception.append(res)
        context['body_reception'] = body_reception
        context['headers_recept'] = headers_recept

        # Remain
        queryset_remain = get_report_by_code(self.request, mycode, ReportProductRemainStock)
        body_remain = get_remain(queryset_remain, dates_today, headers_recept, district=context['object'])
        context['body_remain'] = body_remain
        context['taux'] = get_per_category_taux(self.request)
        context['recus'] = total_received(self.request, mycode)
        return context


# CDS
class CDSCreateView(CreateView):
    model = CDS
    form_class = CDSForm


class CDSListView(ListView):
    model = CDS
    paginate_by = 1000

    def get_queryset(self):
        """Returns Province that belong to the current user"""
        mycode = myfacility(self.request)
        if not mycode['mycode']:
            return CDS.objects.all()
        else:
            if len(mycode['mycode'])< 3:
                return CDS.objects.filter(district__province__code=mycode['mycode'])
            elif 3 <= len(mycode['mycode'])<=4 :
                return CDS.objects.filter(district__code=mycode['mycode'])
            else:
                return CDS.objects.filter(code=mycode['mycode'])


class CDSDetailView(DetailView):
    model = CDS

    def get_context_data(self, **kwargs):
        context = super(CDSDetailView, self).get_context_data(**kwargs)
        mycode = str(context['object'].code)
        pop_total = CampaignCDS.objects.filter(cds__code=mycode)
        if not pop_total:
            pop_total = {}
            pop_total['population_cible'] = 0
        else:
            pop_total = pop_total.latest('id')
        # beneficiaires
        headers_benef = CampaignBeneficiary.objects.all().annotate(beneficiaires=F('beneficiary__designation')).values('beneficiaires').distinct().order_by("id")
        queryset_benef = get_report_by_code(self.request, mycode, ReportBeneficiary)
        dates_benef = queryset_benef.values('reception_date').distinct().order_by('reception_date')
        body_benef = []
        if queryset_benef:
            body_benef = get_benef(queryset_benef, dates_benef, headers_benef)
        # reception
        headers_recept = CampaignProduct.objects.all().annotate(products=F('product__name')).values('products').distinct().order_by('order_in_sms')
        queryset_reception = get_report_by_code(self.request, mycode, ReportProductReception)
        dates_reception = queryset_reception.values('reception_date').distinct().order_by('reception_date')
        body_reception = []
        if queryset_reception:
            body_reception = get_reception(queryset_reception, dates_reception, headers_recept)
        # Remain
        queryset_remain = get_report_by_code(self.request, mycode, ReportProductRemainStock)
        dates_remain = queryset_remain.values('concerned_date').distinct().order_by('concerned_date')
        body_remain = []
        if queryset_remain:
            body_remain = get_remain(queryset_remain, dates_remain, headers_recept, cds=context['object'])
        context['body_benef'] = body_benef
        context['body_reception'] = body_reception
        context['body_remain'] = body_remain
        context['headers_recept'] = headers_recept
        context['headers_benef'] = headers_benef
        context['pop_total'] = pop_total
        context['taux'] = get_per_category_taux(self.request)
        context['estimation'] = estimate(self.request, mycode)
        context['recus'] = total_received(self.request, mycode)
        return context


# ProfileUser
class UserSignupView(CreateView):
    form_class = UserCreationMultiForm
    template_name = 'registration/create_profile.html'

    def get_success_url(self, user):
        return reverse('profile_user_detail', kwargs={'pk': user})

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
                messages.success(self.request, _('Profile created and mail sent to %(email)s.') % {'email':user.email} )
            except:
                messages.success(self.request, _('Unable to send mail  to %(email)s.') % {'email':user.email})
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
    actions = ('read', 'list')
    model = Campaign
    permissions = False

    class List(SmartListView):
        search_fields = ('going_on__icontains', )
        default_order = 'going_on'

    class Create(SmartCreateView):
        form_class = CampaignForm1

        def form_valid(self, form):
            messages.success(self.request, _('Campaign created %(email)s.') % {'email': form.cleaned_data['name']})
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
    actions = ('read', 'list')
    model = Beneficiaire

    class List(SmartListView):
        search_fields = ('designation__icontains', )
        default_order = 'designation'


# Product
class ProductCRUDL(SmartCRUDL):
    actions = ('read', 'list')
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
        search_fields = ('beneficiary__designation__icontains', )
        default_order = 'beneficiary'


# CampaignBeneficiaryProduct
class CampaignBeneficiaryProductCRUDL(SmartCRUDL):
    actions = ('read', 'list')
    model = CampaignBeneficiaryProduct

    class List(SmartListView):
        search_fields = ('campaign_beneficiary__beneficiary__designation__icontains', 'campaign_product__product__name__icontains')
        default_order = 'campaign_beneficiary'


# CampaignProduct
class CampaignProductCRUDL(SmartCRUDL):
    actions = ('read', 'list')
    model = CampaignProduct

    class List(SmartListView):
        search_fields = ('product__name__icontains', )
        default_order = 'product'


# CampaignCDS
class CampaignCDSCRUDL(SmartCRUDL):
    actions = ('read', 'list')
    model = CampaignCDS

    class List(SmartListView):
        fields = ('cds', 'population_cible', 'cds.district.name', 'cds.district.province.name')
        search_fields = ('cds__name__icontains', 'cds__district__name__icontains', 'cds__district__province__name__icontains')
        default_order = 'cds'


# CampaignProduct
class ReportCRUDL(SmartCRUDL):
    actions = ('read', 'list')
    model = Report

    class List(SmartListView):
        fields = ('text', 'reporting_date', 'concerned_date',  'category', 'cds', 'cds.district', 'cds.district.province')
        search_fields = ('text__icontains', 'cds__name__icontains', 'cds__district__name__icontains', 'cds__district__province__name__icontains')
        default_order = 'cds'


# ProfileUser
class ProfileUserCRUDL(SmartCRUDL):
    actions = ('update', 'list', 'read', 'delete')
    model = ProfileUser

    class List(SmartListView):
        fields = ('user', 'telephone', 'user.email', 'level', 'moh_facility')
        search_fields = ('user__name__icontains', 'telephone__icontains', 'user__email__icontains')
        default_order = 'user'

# Campaign
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
                CampaignProduct.objects.get_or_create(campaign=campaign, product=i['product'], order_in_sms=i['order_in_sms'])
                products.add(i['product'])
                orders.add(i['order_in_sms'])

        beneficiaries, orders = set(), set()
        for i in form_dict['beneficiary'].cleaned_data:
            if (i != {}) and (i['beneficiary'] not in beneficiaries) and (i['order_in_sms'] not in orders):
                CampaignBeneficiary.objects.get_or_create(campaign=campaign, beneficiary=i['beneficiary'], order_in_sms=i['order_in_sms'])
                beneficiaries.add(i['beneficiary'])
                orders.add(i['order_in_sms'])

        return HttpResponseRedirect(campaign.get_absolute_url())


@login_required
def initialise_data(request, **kwargs):
    mycode = myfacility(request)
    if 'cds' in kwargs:
        mycode['mycode'] = kwargs.get('cds').code
    if not mycode['mycode'] and not request.user.groups.filter(name='CEN').exists() and not request.user.is_superuser:
        messages.warning(request, _('You have no valid MoH facility attached to \
            your profile. Please contact the Admin'))
        url = reverse('profile_user_detail', kwargs={'pk': mycode['myprofile'].id})
        return HttpResponseRedirect(url)

    # pop total
    pop_total = get_pop_total(request, mycode['mycode'])

    # beneficiaires
    headers_benef = CampaignBeneficiary.objects.all().annotate(beneficiaires=F('beneficiary__designation')).values('beneficiaires').distinct().order_by("id")
    headers_recept = CampaignProduct.objects.all().annotate(products=F('product__name')).values('products').distinct().order_by('order_in_sms')
    taux = get_per_category_taux(request)

    return {"mycode": mycode, "pop_total": pop_total, "headers_benef": headers_benef, "headers_recept": headers_recept, "taux": taux}


@login_required
def get_reports(request, **kwargs):
    searchform = SearchBenef(request)
    initial_data = initialise_data(request, **kwargs)
    mycode = initial_data["mycode"]
    pop_total = initial_data["pop_total"]
    headers_benef = initial_data["headers_benef"]
    headers_recept = initial_data["headers_recept"]
    taux = initial_data["taux"]
    queryset_benef = get_report_by_code(request, mycode['mycode'], ReportBeneficiary)
    dates_benef = []
    body_benef = []
    if not queryset_benef:
        pass
    else:
        dates_benef = queryset_benef.values('reception_date').distinct().order_by('reception_date')
        body_benef = get_benef(queryset_benef, dates_benef, headers_benef)
    # reception
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
    recus = total_received(request, mycode['mycode'])

    return render(request, "ssme_activities/reports.html", {'body_benef': body_benef, 'headers_benef': headers_benef, 'headers_recept': headers_recept, 'body_reception': body_reception, 'body_remain': body_remain, 'pop_total': pop_total, 'taux': taux, 'recus': recus, 'form': searchform})


@login_required
def get_reports_by_benef(request, **kwargs):
    initial_data = initialise_data(request, **kwargs)
    mycode = initial_data["mycode"]
    pop_total = initial_data["pop_total"]
    headers_benef = initial_data["headers_benef"]
    taux = initial_data["taux"]
    # for i in headers_benef:
    #     i['colspan'] = len(CampaignBeneficiaryProduct.objects.filter(campaign_beneficiary__beneficiary__designation=i['beneficiaires']))
    #     i['products'] = CampaignBeneficiaryProduct.objects.filter(campaign_beneficiary__beneficiary__designation=i['beneficiaires']).annotate(product=F('campaign_product__product__name')).values('product')
    queryset_benef = get_report_by_code(request, mycode['mycode'], ReportBeneficiary)
    dates_benef = []
    body_benef = []
    if not queryset_benef:
        pass
    else:
        dates_benef = queryset_benef.values('reception_date').distinct().order_by('reception_date')
        body_benef = get_benef(queryset_benef, dates_benef, headers_benef)

    return render(request, "ssme_activities/reports_by_benef.html", {
        'body_benef': body_benef, 'headers_benef': headers_benef,
        'pop_total': pop_total, 'taux': taux})


@login_required
def get_reports_by_received(request, **kwargs):
    initial_data = initialise_data(request, **kwargs)
    mycode = initial_data["mycode"]
    pop_total = initial_data["pop_total"]
    headers_benef = initial_data["headers_benef"]
    taux = initial_data["taux"]
    headers_recept = initial_data["headers_recept"]
    # reception
    queryset_reception = get_report_by_code(request, mycode['mycode'], ReportProductReception)
    dates_reception = []
    body_reception = []
    if not queryset_reception:
        pass
    else:
        dates_reception = queryset_reception.values('reception_date').distinct().order_by('reception_date')
        body_reception = get_reception(queryset_reception, dates_reception, headers_recept)

    return render(request, "ssme_activities/reports_by_received.html", {
        'body_reception': body_reception, 'headers_benef': headers_benef,
        'headers_recept': headers_recept, 'pop_total': pop_total, 'taux': taux}
        )


@login_required
def get_reports_by_remaining(request, **kwargs):
    initial_data = initialise_data(request, **kwargs)
    mycode = initial_data["mycode"]
    pop_total = initial_data["pop_total"]
    headers_benef = initial_data["headers_benef"]
    taux = initial_data["taux"]
    headers_recept = initial_data["headers_recept"]
    # Remain
    queryset_remain = get_report_by_code(request, mycode['mycode'], ReportProductRemainStock)
    dates_remain = []
    body_remain = []
    if not queryset_remain:
        pass
    else:
        dates_remain = queryset_remain.values('concerned_date').distinct().order_by('concerned_date')
        body_remain = get_remain(queryset_remain, dates_remain, headers_recept)
    recus = total_received(request, mycode['mycode'])

    return render(request, "ssme_activities/reports_by_remaining.html", {
        'body_remain': body_remain, 'headers_benef': headers_benef,
        "recus": recus, 'headers_recept': headers_recept,
        'pop_total': pop_total, 'taux': taux}
        )


@login_required
def get_reports_by_rates(request, **kwargs):
    initial_data = initialise_data(request, **kwargs)
    mycode = initial_data["mycode"]
    pop_total = initial_data["pop_total"]
    recus = total_received(request, mycode['mycode'])

    return render(request, "ssme_activities/reports_by_rates.html", {
        "recus": recus, 'pop_total': pop_total}
        )


# Benef
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


@login_required
def get_benef_in_json(request):
    mycode = myfacility(request)
    benef = get_report_by_code(request, mycode['mycode'], ReportBeneficiary)
    data = json.dumps([dict(item) for item in benef.annotate(beneficiaires=F('campaign_beneficiary__beneficiary__designation')).annotate(province=F('report__cds__district__province__name')).annotate(pop_servie=F('received_number')).annotate(cds=F('report__cds__name')).annotate(district=F('report__cds__district__name')).values('beneficiaires',  'reception_date', 'pop_servie', 'province', 'district', 'cds')], default=date_handler)

    return HttpResponse(data, content_type='application/json')


# Recus
@login_required
def get_recus_in_json(request):
    mycode = myfacility(request)
    recus = get_report_by_code(request, mycode['mycode'], ReportProductReception)
    data = json.dumps([dict(item) for item in recus.annotate(products=F('campaign_product__product__name')).annotate(province=F('report__cds__district__province__name')).annotate(quantite_recue=F('received_quantity')).annotate(district=F('report__cds__district__name')).annotate(cds=F('report__cds__name')).values('products',  'reception_date', 'quantite_recue', 'province', 'district', 'cds')], default=date_handler)

    return HttpResponse(data, content_type='application/json')


@login_required
def get_final_in_json(request):
    mycode = myfacility(request)
    finals = get_report_by_code(request, mycode['mycode'], ReportProductRemainStock)
    data = json.dumps([dict(item) for item in finals.annotate(products=F('campaign_product__product__name')).annotate(province=F('report__cds__district__province__name')).annotate(quantite_restante=F('remain_quantity')).annotate(district=F('report__cds__district__name')).annotate(cds=F('report__cds__name')).values('products',  'concerned_date', 'quantite_restante', 'province', 'district', 'cds')], default=date_handler)

    return HttpResponse(data, content_type='application/json')

##########
# Estimations  #
##########


def estimate(request, cds=''):
    headers_benef = CampaignBeneficiary.objects.all().annotate(beneficiaires=F('beneficiary__designation')).values('beneficiaires').distinct().order_by("id")
    benefs = []
    for h in headers_benef:
        benef = ReportBeneficiary.objects.filter(report__cds__code=cds, campaign_beneficiary__beneficiary__designation=h['beneficiaires']).aggregate(Sum('received_number'))
        for i in CampaignBeneficiaryProduct.objects.filter(campaign_beneficiary__beneficiary__designation=h['beneficiaires']):
            if benef['received_number__sum']:
                benef.update({str(i.campaign_product.product.name): int(i.dosage * benef['received_number__sum'])})
            else:
                benef.update({str(i.campaign_product.product.name): 0})
        benef.update(h)
        benefs.append(benef)
    return convert(benefs)


def total_received(request, mycode=''):
    headers_recept = CampaignProduct.objects.all().annotate(products=F('product__name')).values('products').distinct()
    recus = {}
    queryset_recu = get_report_by_code(request, mycode, ReportProductReception)
    for h in headers_recept:
        recu = queryset_recu.filter(campaign_product__product__name=h['products']).aggregate(Sum('received_quantity'))

        recus.update({str(h['products']): recu['received_quantity__sum']})
    return convert(recus)


@login_required
def participation(request):
    response_data = {}

    #if not request.GET["camp_id"] or request.GET["camp_id"] == -1:
    if int(request.GET["camp_id"]) == -1 or request.GET["camp_id"] == None:
        the_last_campaign = Campaign.objects.all().order_by('-id')[0]
    else:
        the_last_campaign = Campaign.objects.get(id=request.GET["camp_id"])

    target_population_for_this_campaign = CampaignCDS.objects.filter(campaign = the_last_campaign).aggregate(Sum('population_cible'))

    the_camp_start_date = the_last_campaign.start_date
    date_of_day_two = the_camp_start_date+datetime.timedelta(days=1)
    date_of_day_three = the_camp_start_date+datetime.timedelta(days=2)
    date_of_day_four = the_camp_start_date+datetime.timedelta(days=3)
    the_camp_end_date = the_last_campaign.end_date

    if(the_last_campaign):
        beneficiaries_4_last_campaign = Beneficiaire.objects.filter(campaignbeneficiary__campaign = the_last_campaign)
        related_campaign_beneficiaries = CampaignBeneficiary.objects.filter(campaign = the_last_campaign).annotate(received_people = Sum('campaignbeneficiaryproduct__reportbeneficiary__received_number')).values()
        response_data = json.dumps(list(related_campaign_beneficiaries), cls=DjangoJSONEncoder)
        rows = json.loads(response_data)
        for r in rows:
            beneficiary = Beneficiaire.objects.get(id = r['beneficiary_id'])
            r["beneficiary_name"] = beneficiary.designation
            r["campaign_start_date"] = the_last_campaign.start_date
            r["campaign_end_date"] = the_last_campaign.end_date

            r["target_population"] = target_population_for_this_campaign["population_cible__sum"]

            received_number_on_first_date = ReportBeneficiary.objects.filter(beneficiaries_per_product__campaign_beneficiary__id = r['id'] ,reception_date = the_camp_start_date).aggregate(Sum('received_number'))
            r["received_on_day_one"] = received_number_on_first_date["received_number__sum"]

            received_number_on_day_2 = ReportBeneficiary.objects.filter(beneficiaries_per_product__campaign_beneficiary__id = r['id'] ,reception_date = date_of_day_two).aggregate(Sum('received_number'))
            r["received_on_day_two"] = received_number_on_day_2["received_number__sum"] + r["received_on_day_one"]

            received_number_on_day_3 = ReportBeneficiary.objects.filter(beneficiaries_per_product__campaign_beneficiary__id = r['id'] ,reception_date = date_of_day_three).aggregate(Sum('received_number'))
            r["received_on_day_three"] = received_number_on_day_3["received_number__sum"] + r["received_on_day_two"]

            received_number_on_day_4 = ReportBeneficiary.objects.filter(beneficiaries_per_product__campaign_beneficiary__id = r['id'] ,reception_date = date_of_day_four).aggregate(Sum('received_number'))
            r["received_on_day_four"] = received_number_on_day_4["received_number__sum"] + r["received_on_day_three"]

        response_data = json.dumps(rows, default=date_handler)
        print("------------------")
        print(response_data)
        return HttpResponse(response_data, content_type="application/json")


class ProvinceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit Province.
    """
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    filter_field = ('')


class DistrictViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit District.
    """
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    lookup_field = 'code'
    filter_fields = ('province__code',)


class CDSViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit CDS.
    """
    queryset = CDS.objects.all()
    serializer_class = CDSSerializer
    lookup_field = 'code'
    filter_fields = ('district__code',)
