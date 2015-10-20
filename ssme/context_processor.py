from ssme_activities.models import CDS, District, Province, ProfileUser

def get_name_of_mohfacility(level='',code=''):
    if level=='CDS':
        return CDS.objects.get(code=code).name
    if level=='BDS':
        return District.objects.get(code=code).name
    if level=='BPS':
        return Province.objects.get(code=code).name
    if level=='CEN':
        return 'Central'

def myfacility(request):
    myprofile = None
    try:
        myprofile, created = ProfileUser.objects.get_or_create(user=request.user)
    except TypeError:
        return {}
    if not created:
        mymoh_facility = get_name_of_mohfacility(myprofile.level, myprofile.moh_facility)

    return {'myprofile':myprofile, 'mycode':myprofile.moh_facility , 'mylevel': myprofile.level, 'mymoh_facility': mymoh_facility  }