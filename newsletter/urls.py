from django.conf.urls import url, patterns
import views

urlpatterns = patterns(
    '',
    url(r'^archive/$', views.archive),
    url(r'^(?P<vol_year>\d+)/(?P<vol_month>\w+)/volume-(?P<volume>\d+)$', views.get_newsletter),
)
