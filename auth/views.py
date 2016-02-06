from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from main.models import UserDetails
from lib.forum_helpers import update_forum_user
import json


# User login view
def user_login(request):
    return render(request, 'auth/login.html')


@login_required
def post_login(request):
    """ Update user profile """
    try:
        # Main User Model
        usr = User.objects.get(email=request.user.email)
        update_forum_user(request)

        usr.first_name = request.user.first_name
        usr.last_name = request.user.last_name
        usr.save()
    except ObjectDoesNotExist:
        print Exception
        return redirect('auth.views.user_login')

    try:
        user_profile = UserDetails.objects.get(user_id=request.user.id)
        if "@google.com" in request.user.email:
            if not user_profile.user_manager_email or not user_profile.team or not user_profile.location or not user_profile.rep_location:
                return redirect('main.views.get_started')
        else:
            if not user_profile.user_manager_email or not user_profile.user_manager_name:
                return redirect('main.views.get_started')
    except ObjectDoesNotExist:
        return redirect('main.views.get_started')

    return redirect('main.views.home')


# User logout view
def user_logout(request):
    logout(request)
    return redirect('auth.views.user_login')


# User Auth Error
def auth_error(request):
    """ Displays Errors """
    email = request.GET.get('email')
    return render(request, 'auth/error.html', {'email': email})


# Check user's email
def check_email(strategy, details, *args, **kwargs):
    email = details.get('email')
    domain = details.get('email').split('@')[1]
    if domain not in settings.SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS:
        if email not in settings.SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS:
            return HttpResponseRedirect(reverse('auth.views.auth_error') + "?email=" + details.get('email'))


def handle_page_not_found(request):
    """ Page not found Page """
    print "404 Page"
    return render_to_response('auth/404.html', locals(), context_instance=RequestContext(request))
    # return render(request, 'auth/404.html')


@login_required
def redirect_domain(request):
    """ Redirect or Swap the domain TAG to WPP and vicevarsa
        for Tag: gtrack.regalix.com
        for WPP: wpp.regalix.com
    """
    redirect_domain = ''
    if 'wpp' in request.get_host():
        redirect_domain = request.get_host().replace('wpp', 'gtrack')
    else:
        redirect_domain = request.get_host().replace('gtrack', 'wpp')

    redirect_domain = request.META['wsgi.url_scheme'] + '://' + redirect_domain

    return HttpResponse(json.dumps(redirect_domain))
