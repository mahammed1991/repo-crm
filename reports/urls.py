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
    url(r'^link-last-meeting/(?P<last_id>\w+)/$', views.link_last_meeting),
    url(r'^thankyou/$', views.meeting_minutes_thankyou),
    # Export meeting minutes
    url(r'^export-meeting-minutes/$', views.export_meeting_minutes),
    url(r'^get-meeting-minutes/$', views.get_meeting_minutes),
    url(r'^generate-link/$', views.generate_link),
    url(r'^export-action-items/$', views.export_action_items),

    # kick-off-program
    url(r'^program-kick-off/$', views.program_kick_off),
    url(r'^kickoff-export/$', views.kickoff_export),
    url(r'^kickoff-export-detail/(?P<program_id>\w+)/$', views.kickoff_export_detail, name='kickoff-export-detail'),
    url(r'^thankyou-kickoff-program/$', views.kickoff_thankyou),
    url(r'^get-kickoff-programs/$', views.get_kickoff_program),
     url(r'^thankyou-tagteam-kickoff-program/$', views.tagteam_kickoff_thankyou),
     url(r'^rlsa-bulk-upload/$', views.rlsa_bulk_upload_report),


)
