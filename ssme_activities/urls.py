from django.conf.urls import patterns, url
from ssme_activities.backend import handel_rapidpro_request

urlpatterns = patterns('',
    url(r'external_request', handel_rapidpro_request, name="handel_request"),
)
