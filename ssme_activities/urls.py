from django.conf.urls import patterns, url
from ssme_activities.backend import handel_rapidpro_request
from ssme_activities.views import *
from django.contrib.auth.decorators import login_required as _


urlpatterns = patterns('',
    url(r'external_request', handel_rapidpro_request, name="handel_request"),
    url(r'^moh_facility/$', moh_facility, name='moh_facility'),
    url(r'^profile_user/$', profile_user, name='profile_user'),
    url(r'^campaigns/$', campaigns, name='campaigns'),
    url(r'^beneficiaries/$', beneficiaries, name='beneficiaries'),

    url(r'^cds/$', _(CDSListView.as_view()), name='cds_list'),
    url(r'^cds/add/$', _(CDSCreateView.as_view()), name='cds_add'),
    url(r'^cds/(?P<pk>\d+)/$', _(CDSDetailView.as_view()), name='cds_detail'),
    # Districts
    url(r'^district/$', _(DistrictListView.as_view()), name='district_list'),
    url(r'^district/add/$', _(DistrictCreateView.as_view()), name='district_add'),
    url(r'^district/(?P<pk>\d+)/$', _(DistrictDetailView.as_view()),
        name='district_detail'),
    # Provinces
    url(r'^province/$', _(ProvinceListView.as_view()), name='province_list'),
    url(r'^province/add/$', _(ProvinceCreateView.as_view()), name='province_add'),
    url(r'^province/(?P<pk>\d+)/$', _(ProvinceDetailView.as_view()),
        name='province_detail'),

    # ProfileUser
    url(r'^register/$', _(UserSignupView.as_view()), name="create_profile"),
    url(r'^profile/(?P<pk>\d+)/$', _(ProfileUserDetailView.as_view()),
        name="profile_user_detail"),
    url(r'^profile_edit/(?P<pk>\d+)/$', _(ProfileUserUpdateView.as_view()),
        name="profileuser_update"),
    url(r'^create_campaign/$', _(CampaignWizard.as_view(FORMS)),
        name="ssme_activities.campaign_create"),

    # Reports
    url(r'^reports/$', get_reports, name="reports"),
    url(r'^reports/benef/$', get_reports_by_benef, name="reports_by_benef"),
    url(r'^reports/received/$', get_reports_by_received,
        name="reports_by_received"),
    url(r'^reports/received/$', get_reports_by_remaining,
        name="reports_by_remaining"),
    url(r'^calcul_benef/$', get_benef_in_json, name="calcul_benef"),
    url(r'^calcul_recus/$', get_recus_in_json, name="calcul_recus"),
    url(r'^calcul_final/$', get_final_in_json, name="calcul_final"),

)

urlpatterns += CampaignCRUDL().as_urlpatterns()
urlpatterns += BeneficiaireCRUDL().as_urlpatterns()
urlpatterns += ProductCRUDL().as_urlpatterns()
urlpatterns += CampaignBeneficiaryCRUDL().as_urlpatterns()
urlpatterns += CampaignBeneficiaryProductCRUDL().as_urlpatterns()
urlpatterns += CampaignProductCRUDL().as_urlpatterns()
urlpatterns += ReportCRUDL().as_urlpatterns()
urlpatterns += ProfileUserCRUDL().as_urlpatterns()
urlpatterns += CampaignCDSCRUDL().as_urlpatterns()
