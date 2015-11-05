from ssme_activities.models import CDS, District, Province, ProfileUser, Campaign, CampaignBeneficiary
from django.db.models import F


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
    campaign = Campaign.objects.filter(going_on=True)
    if not campaign:
        campaign = ['no campaign']

    return {'myprofile':myprofile, 'mycode':myprofile.moh_facility , 'mylevel': myprofile.level, 'mymoh_facility': mymoh_facility, 'mycampaign': campaign[0] }

def get_per_category_taux(request):
    headers_benef = CampaignBeneficiary.objects.filter(campaign__going_on=True).annotate(beneficiaires=F('beneficiary__designation')).values('beneficiaires').distinct().order_by("id")
    taux = {}
    # import ipdb; ipdb.set_trace()
    for i in headers_benef:
        taux.update({str(i['beneficiaires']): CampaignBeneficiary.objects.filter(beneficiary__designation=i['beneficiaires'])[0].pourcentage_attendu})
    return taux