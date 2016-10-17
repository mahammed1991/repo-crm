from django.conf.urls import url, patterns
import views

urlpatterns = patterns(
    '',
    url(r'^portal-crm/agent/$', views.crm_management),
    url(r'^portal-crm/manager/$', views.manager_home),
)
