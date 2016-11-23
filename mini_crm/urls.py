from django.conf.urls import url, patterns
import views

urlpatterns = patterns(
    '',
    url(r'^all-leads/$', views.crm_management, name="all-leads"),
    url(r'^myleads/$', views.crm_agent),
    url(r'^lead-details/(?P<lid>[0-9]+)/(?P<sf_lead_id>\w+)/(?P<ctype>\w+)$', views.lead_details),
    url(r'^lead-owner-email', views.lead_owner_avalibility),
    url(r'^update-lead/$', views.update_lead),
    url(r'^add-lead-comment/$', views.add_lead_comment),
    url(r'^lead-history/$', views.lead_history),
    url(r'^search-leads/', views.search_leads),
    url(r'^crm-agents/emails/$', views.get_crm_agents_emails),
    url(r'^clone-lead/$', views.clone_lead),
    url(r'^delete-lead/(?P<lid>[0-9]+)/(?P<ctype>\w+)$', views.delete_lead, name="delete-lead"),
    url(r'^get-lead-history/$', views.get_lead_history),
    url(r'^save-image-file/$', views.save_image_file),
    url(r'^download-image-file/', views.download_image_file),
    url(r'^get-lead-sub-status/$', views.get_lead_sub_status),
    url(r'^get-feed-optimisation-sub-status/$', views.get_feed_optimisation_sub_status),
    url(r'^user-appointments/$', views.user_appointmnets),
)
