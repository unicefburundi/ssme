from django.conf.urls import patterns, url
from ssme_activities.backend import handel_rapidpro_request
from ssme_activities.views import *

urlpatterns = patterns('',
    url(r'external_request', handel_rapidpro_request, name="handel_request"),
    url(r'^moh_facility/$', moh_facility, name='moh_facility'),
    url(r'^profile_user/$', profile_user, name='profile_user'),
    url(r'^campaigns/$', campaigns, name='campaigns'),
    url(r'^beneficiaries/$', beneficiaries, name='beneficiaries'),

    url(r'^cds/$', CDSListView.as_view(), name='cds_list'),
    url(r'^cds/add/$', CDSCreateView.as_view(), name='cds_add'),
    url(r'^cds/(?P<pk>\d+)/$', CDSDetailView.as_view(), name='cds_detail'),
    #Districts
    url(r'^district/$', DistrictListView.as_view(), name='district_list'),
    url(r'^district/add/$', DistrictCreateView.as_view(), name='district_add'),
    url(r'^district/(?P<pk>\d+)/$', DistrictDetailView.as_view(), name='district_detail'),
    #Provinces
    url(r'^province/$', ProvinceListView.as_view(), name='province_list'),
    url(r'^province/add/$', ProvinceCreateView.as_view(), name='province_add'),
    url(r'^province/(?P<pk>\d+)/$', ProvinceDetailView.as_view(), name='province_detail'),
)
