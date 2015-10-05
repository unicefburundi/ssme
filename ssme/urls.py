from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ssme/', include('ssme_activities.urls')),
    url(r'^accounts/', include('authtools.urls')),
    url(r'^dashboard/$', 'ssme.views.dashboard', name='dashboard'),
    url(r'^$', 'ssme.views.landing', name='landing'),
) +  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#In development, static files should be served from app static directories
if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()

