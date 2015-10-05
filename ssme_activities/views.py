from django.shortcuts import render

def dashboard(request):
    return render(request, 'base_layout.html')

def moh_facility(request):
    return render(request, 'moh_facility.html')
