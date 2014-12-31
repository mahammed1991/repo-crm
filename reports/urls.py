from django.conf.urls import url, patterns
import views

urlpatterns = patterns(
    '',
    url(r'^$', views.reports),
    url(r'^get-reports$', views.get_reports),
    url(r'^current-quarter-report$', views.get_current_quarter_report),
    url(r'^download-leads$', views.download_leads),
    url(r'^get-trends-reports$', views.get_trends_reports),
    url(r'^download-timezones-by_location$', views.download_timezones_by_location)
)
