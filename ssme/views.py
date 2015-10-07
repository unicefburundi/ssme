from django.shortcuts import render
from ssme_activities.models import Province, District, CDS
from django.http import JsonResponse

def landing(request):
    return render(request, 'landing_page.html')

def get_by_level(request, level='CEN'):
    results_dict = {}
    results = None
    if level == 'BPS':
        results = Province.objects.all().order_by('name')
    if level == 'BDS':
        results = District.objects.all().order_by('name')
    if level == 'CDS':
        results = CDS.objects.all().order_by('name')
    if level in ['CEN', '']  :
        return JsonResponse([{'':'-----'}], safe=False)
    for result in results:
        results_dict[result.code] = result.name
    return JsonResponse([results_dict], safe=False)
