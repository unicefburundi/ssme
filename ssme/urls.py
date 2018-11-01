from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = patterns(
    "",
    url(r"^admin/", include(admin.site.urls)),
    url(r"^ssme/", include("ssme_activities.urls")),
)

urlpatterns += i18n_patterns(
    url(r"^accounts/", include("authtools.urls")),
    url(r"^users/", include("smartmin.users.urls")),
    url(
        r"^get_by_level/(?P<level>\w+)/$",
        "ssme.views.get_by_level",
        name="get_by_level",
    ),
    url(r"^dashboard/$", "ssme_activities.views.dashboard", name="dashboard"),
    url(
        r"^dashboard/participation/$",
        "ssme_activities.views.participation",
        name="participation",
    ),
    url(
        r"^dashboard/fetchbeneficiaries/$",
        "ssme_activities.views.fetchbeneficiaries",
        name="fetchbeneficiaries",
    ),
    url(r"^$", "ssme.views.landing", name="landing"),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
