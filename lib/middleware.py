from json import loads

from requests import request as request_call
from django.core.exceptions import ObjectDoesNotExist
from social.exceptions import AuthForbidden
from django.shortcuts import redirect
from main.models import UserDetails


class SetProfilePicture(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        # get profile picture from google
        if request.user.is_authenticated() and 'profile_image' not in request.session:
            try:
                user_profile = request.user.social_auth.get(uid=request.user.email)
                user_access_token = user_profile.extra_data['access_token']

                user_profile_from_google = request_call(
                    'GET',
                    'https://www.googleapis.com/oauth2/v1/userinfo?access_token=' + user_access_token
                )

                if user_profile_from_google.status_code == 200:
                    response = loads(user_profile_from_google.text)
                    image_url = response['picture']
                else:
                    image_url = '/static/images/login_pic.png'
                request.session['profile_image'] = image_url
                try:
                    user_profile = UserDetails.objects.get(user_id=request.user.id)
                    user_profile.profile_photo_url = image_url
                    user_profile.save()
                    request.profile_image_url = image_url
                    request.session['profile'] = user_profile
                except ObjectDoesNotExist:
                    pass
            except ObjectDoesNotExist:
                pass

        response = view_func(request, *view_args, **view_kwargs)
        return response


class StandardExceptionMiddleware(object):

    def process_exception(self, request, exception):
        if isinstance(exception, AuthForbidden):
            return redirect('auth.views.user_login')
