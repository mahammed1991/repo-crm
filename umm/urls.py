from django.conf.urls import url, patterns
import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home),
    url(r'^india/$', views.umm_india),
    url(r'^india-quality/$', views.umm_india_quality),
    url(r'^india-productivity/$', views.umm_india_productivity),
    url(r'^customized-analysis/$', views.umm_customized_analysis),
    url(r'^upload-excel/$', views.manage_excel),
)
