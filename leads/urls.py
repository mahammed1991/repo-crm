from django.conf.urls import url, patterns
import views

urlpatterns = patterns(
    '',
    url(r'^lead-form/$', views.lead_form),
    url(r'^shopping-campaign-setup-lead-form/$', views.shopping_campaign_setup_lead_form),
    url(r'^shopping-campaign-lead-form/$', views.shopping_campaign_lead_form),
    url(r'^leads-list/$', views.leads_list),
    url(r'^leads-report/$', views.leads_report),
    url(r'^thankyou/$', views.thankyou),
    url(r'^day-light-changes/$', views.day_light_changes),
    url(r'^manage-leads/$', views.manage_leads),
    url(r'^upload-leads/$', views.upload_leads),
    url(r'^migrate-leads/$', views.migrate_leads),
    url(r'^get-lead/(?P<cid>[\w -]+)$', views.get_lead),
    url(r'^lead-summary/$', views.get_lead_summary),
    url(r'^lead-summary/(?P<lid>[0-9]+)$', views.get_lead_summary),
    url(r'^create-chat/$', views.create_chat_message),
    url(r'^get-chat/$', views.get_chat_message_by_lead),
)
