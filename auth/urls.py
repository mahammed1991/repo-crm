from django.conf.urls import patterns, url, include
import views

urlpatterns = patterns(
    '',
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login$', views.user_login),
    url(r'^logout$', views.user_logout),
    url(r'^error$', views.auth_error),
    url(r'^post_login/$', 'auth.views.post_login'),
    url(r'^redirect_domain/$', 'auth.views.redirect_domain'),
)
