from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView
from django.contrib import admin

admin.autodiscover()

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

    #urls for accessing analytics file to retrive credntials from google
    url(r'^analytics\.txt', TemplateView.as_view(template_name='analytics.txt')),
    url(r'^main/home/analytics\.txt', TemplateView.as_view(template_name='analytics.txt')),
    url(r'^robots\.txt', TemplateView.as_view(template_name='robots.txt')),
)
