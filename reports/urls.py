from django.conf.urls import url, patterns
import views

urlpatterns = patterns(
    '',
    url(r'^$', views.reports),
    url(r'^get-reports$', views.get_reports),
    url(r'^current-quarter-report$', views.get_current_quarter_report),
    url(r'^download-leads$', views.download_leads),
    url(r'^get-trends-reports$', views.get_trends_reports),
    url(r'^download-timezones-by_location$', views.download_timezones_by_location),
    url(r'^get_new_reports$', views.get_new_reports),
    url(r'^get-countries$', views.get_countries),
    url(r'^get-download-report$', views.get_download_report),
    url(r'^get-user-name$', views.get_user_name),
    # url(r'^get-program-location$', views.get_program_by_location),
    url(r'^wpp/$', views.wpp_reports),
    url(r'^wpp/get-wpp-reports/$', views.get_wpp_reports),
    url(r'^wpp/master-list/$', views.wpp_master_list),
    url(r'^wpp/call-audit-sheet/$', views.call_audit_sheet),
    url(r'^google-doc/$', views.google_doc),
    url(r'^user-events/$', views.user_events),
    url(r'^csat-reports/$', views.csat_reports),
    url(r'^picasso/$', views.picasso_reports),
    url(r'^download-picasso-report/$', views.download_picasso_report),
    url(r'^reports-new$', views.reports_new),
    url(r'^get_selected_new_reports$', views.get_selected_new_reports),
    url(r'^get_selected_view_type$', views.get_selected_report_view),
    # Meeting page URL
    url(r'^meeting-minutes/$', views.meeting_minutes),
)
