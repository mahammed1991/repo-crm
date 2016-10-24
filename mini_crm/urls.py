from django.conf.urls import url, patterns
import views
from django.views.generic import RedirectView, TemplateView

urlpatterns = patterns(
    '',
    url(r'^all-leads/$', views.crm_management),
    url(r'^myleads/$', views.crm_agent),
    url(r'^lead_history/$',views.lead_history)
)
