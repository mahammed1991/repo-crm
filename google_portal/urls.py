from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)

from django.contrib import admin
admin.autodiscover()

handler400 = 'main.views.bad_request'
handler403 = 'main.views.permission_denied'
handler404 = 'main.views.page_not_found'
handler500 = 'main.views.server_error'

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'main.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', RedirectView.as_view(url='/main/')),
    url(r'^main/', include('main.urls')),
    url(r'^auth/', include('auth.urls')),
    url(r'^leads/', include('leads.urls')),
    url(r'^newsletter/', include('newsletter.urls')),
    url(r'^representatives/', include('representatives.urls')),
    url(r'^reports/', include('reports.urls')),
    # url(r'^email/(?P<name>\w+)$', views.email_templates),
    url(r'^forums/', include('forum.urls')),
    url(r'^umm/', include('umm.urls')),
)
