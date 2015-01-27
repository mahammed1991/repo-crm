from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from forum.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from forum.actions import UserLoginAction, UserJoinsAction
from django.template import RequestContext
from main.models import UserDetails


# User login view
def user_login(request):
    return render(request, 'auth/login.html')


@login_required
def post_login(request):
    """ Update user profile """
    try:
        username = request.user.username.split('@')[0]

        # Main User Model
        request.user.save()

        # Customise User Model
        user = User.objects.get(username=username)
        user.user_ptr = request.user
        user.save()
    except ObjectDoesNotExist:
        obj = User()
        obj.user_ptr = request.user
        obj.email_isvalid = True
        obj.last_seen = request.user.last_login
        obj.username = request.user.username if '@' not in request.user.username else request.user.username.split('@')[0]
        obj.real_name = "%s %s" % (request.user.first_name, request.user.last_name)
        obj.is_active = request.user.is_active
        obj.email = request.user.email
        obj.profile_image_url = request.session['profile_image'] if 'profile_image' in request.session else ''
        obj.save()
        # UserLoginAction(user=obj, ip=request.META['REMOTE_ADDR']).save()
        # UserJoinsAction(user=obj).save()
        return redirect('main.views.get_started')
    try:
        user_profile = UserDetails.objects.get(user_id=request.user.id)
        if not user_profile.phone and not user_profile.user_manager_name and not user_profile.user_manager_email and user_profile.team and user_profile.location:
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
    email = details.get('email').split('@')[1]
    if email not in settings.SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS:
        return HttpResponseRedirect(reverse('auth.views.auth_error') + "?email=" + details.get('email'))


def handle_page_not_found(request):
    """ Page not found Page """
    print "404 Page"
    return render_to_response('auth/404.html', locals(), context_instance=RequestContext(request))
    #return render(request, 'auth/404.html')
