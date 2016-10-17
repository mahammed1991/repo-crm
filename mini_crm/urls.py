from django.conf.urls import url, patterns
import views
from django.views.generic import RedirectView, TemplateView

urlpatterns = patterns(
    '',
    (r'^$', RedirectView.as_view(url='/crm/management/')),
    url(r'^management/$', views.crm_management),
)
