from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User, Group
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
    try:
        grp = Group.objects.get(name='WPP')
    except ObjectDoesNotExist:
        grp = None
    if request.session['redirect_domain'] == 'TAG':
        request.user.groups.remove(grp.id) if grp else request.user.groups
        redirect_domain = settings.TAG_URL
    if request.session['redirect_domain'] == 'WPP':
        request.user.groups.add(grp.id) if grp else request.user.groups
        redirect_domain = settings.WPP_URL

    return HttpResponse(json.dumps(redirect_domain))


@login_required
def current_domain(request):
    """ Redirect or Swap the domain TAG to WPP and vicevarsa
        for Tag: gtrack.regalix.com
        for WPP: wpp.regalix.com
    """
    change_url = 0
    current_domain = request.get_host()
    if request.session['redirect_domain'] == 'TAG':
        if 'gtrack' in request.get_host():
            current_domain = request.get_host().replace('gtrack.', 'wpp.')
            change_url = 1
    elif request.session['redirect_domain'] == 'WPP':
        if 'wpp' in request.get_host():
            current_domain = request.get_host().replace('wpp.', 'gtrack.')
            change_url = 1
    return HttpResponse(json.dumps({'session': request.session['redirect_domain'], 'current_domain': current_domain, 'change_url': change_url, 'url_scheme': request.META['wsgi.url_scheme'], }))
