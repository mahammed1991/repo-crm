from django.conf.urls import url, patterns
import views
from django.views.generic import RedirectView, TemplateView

urlpatterns = patterns(
    '',
    url(r'^all-leads/$', views.crm_management),
    url(r'^myleads/$', views.crm_agent),
    url(r'^lead-details/(?P<lid>[0-9]+)/(?P<sf_lead_id>\w+)/(?P<ctype>\w+)$',views.lead_details),
    url(r'^lead-owner-email',views.lead_owner_avalibility),
    url(r'^lead-history/$',views.lead_history),
    url(r'^search-leads/', views.search_leads),
    url(r'^crm-agents/emails/$',views.get_crm_agents_emails),
    url(r'^clone-lead/$', views.clone_lead),
)
