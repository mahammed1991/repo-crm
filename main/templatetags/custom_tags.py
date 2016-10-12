from django import template
from main.models import OlarkChatGroup
from django.contrib.auth.models import Group

register = template.Library()


@register.simple_tag
def olark_group_script(user):
    try:
        if user.email:
            chat_group = OlarkChatGroup.objects.filter(google_rep__in=[user])
            if len(chat_group) > 0:
                return chat_group[0].olark_script

            if user.profile.team and user.profile.location:

                chat_group = OlarkChatGroup.objects.filter(programs__in=[user.profile.team], target_location__in=[user.profile.location])
                if len(chat_group) > 0:
                    return chat_group[0].olark_script
        else:
            return "<script>olark('api.box.hide');</script>"
    except Exception:
        return "<script>olark('api.box.hide');</script>"


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
