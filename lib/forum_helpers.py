from forum.models import User
from django.core.exceptions import ObjectDoesNotExist
from forum.actions import UserLoginAction, UserJoinsAction


def update_forum_user(request):
    """ Create or Update Forum User model """

    try:
        # Customise User Model
        # username = request.user.username.split('@')[0]
        user = User.objects.get(user_ptr_id=request.user.id)
        user.user_ptr = request.user
        user.save()
    except ObjectDoesNotExist:
        obj = User()
        obj.user_ptr = request.user
        obj.email_isvalid = True

        obj.last_seen = request.user.last_login
        obj.username = request.user.username if '@' not in request.user.username else request.user.username.split('@')[0]
        obj.real_name = "%s %s" % (request.user.first_name, request.user.last_name)
        # obj.is_active = request.user.is_active
        obj.email = request.user.email
        obj.profile_image_url = request.session['profile_image'] if 'profile_image' in request.session else ''
        obj.save()
        # UserLoginAction(user=obj, ip=request.META['REMOTE_ADDR']).save()
        # UserJoinsAction(user=obj).save()
