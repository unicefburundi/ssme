from ssme_activities.models import CDS, District, Province, ProfileUser, Campaign, CampaignBeneficiary
from django.db.models import F
import collections
from django.conf import settings


def get_name_mohfacility(level='',code=''):
    if level=='CDS':
        return CDS.objects.get(code=code)
    if level=='BDS':
        return District.objects.get(code=code)
    if level=='BPS':
        return Province.objects.get(code=code)
    if level=='CEN':
        return 'Central'

def myfacility(request):
    myprofile = None
    try:
        myprofile, created = ProfileUser.objects.get_or_create(user=request.user)
    except TypeError:
        return {}
    if not created:
        mymoh_facility = get_name_mohfacility(myprofile.level, myprofile.moh_facility)
    #import ipdb; ipdb.set_trace()
    campaign = Campaign.objects.latest('end_date')
    if not campaign:
        campaign = ['no campaign']

    return {'myprofile':myprofile, 'mycode':myprofile.moh_facility , 'mylevel': myprofile.level, 'mymoh_facility': mymoh_facility, 'mycampaign': campaign }

def get_per_category_taux(request):
    headers_benef = CampaignBeneficiary.objects.all().annotate(beneficiaires=F('beneficiary__designation')).values('beneficiaires').distinct().order_by("id")
    taux = {}
    for i in headers_benef:
        taux.update({str(i['beneficiaires']): CampaignBeneficiary.objects.filter(beneficiary__designation=i['beneficiaires'])[0].pourcentage_attendu})
    return taux

def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

def add_elements_in_dict(list):
    somme = collections.Counter(list[0])
    for i in list[1:]:
        somme += collections.Counter(i)
    return dict(somme)

def google_analytics(request):
    """
    Use the variables returned in this function to
    render your Google Analytics tracking code template.
    """
    ga_prop_id = getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', False)
    ga_domain = getattr(settings, 'GOOGLE_ANALYTICS_DOMAIN', False)
    if not settings.DEBUG and ga_prop_id and ga_domain:
        return {
            'GOOGLE_ANALYTICS_PROPERTY_ID': ga_prop_id,
            'GOOGLE_ANALYTICS_DOMAIN': ga_domain,
        }
    return {}
