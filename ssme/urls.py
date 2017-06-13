from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.i18n import i18n_patterns
from controlcenter.views import controlcenter

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/dashboard/', controlcenter.urls),
    url(r'^ssme/', include('ssme_activities.urls')),
    )

urlpatterns += i18n_patterns(
    url(r'^accounts/', include('authtools.urls')),
    url(r'^users/', include('smartmin.users.urls')),
    url(r'^get_by_level/(?P<level>\w+)/$', 'ssme.views.get_by_level', name='get_by_level'),
    url(r'^dashboard/$', 'ssme_activities.views.dashboard', name='dashboard'),
    url(r'^explorer/', include('explorer.urls')),
    url(r'^$', 'ssme.views.landing', name='landing'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# In development, static files should be served from app static directories
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
