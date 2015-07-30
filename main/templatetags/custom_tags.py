from django import template
from main.models import OlarkChatGroup
from django.contrib.auth.models import Group

register = template.Library()


@register.simple_tag
def olark_group_script(user):

    # operator_groups = OlarkChatGroup.objects.all()

    # for operator_group in operator_groups:
        # teams = [t.team_name for t in operator_group.programs.filter()]
        # locations = [l.location_name for l in operator_group.target_location.filter()]
        # emails = [usr.email for usr in operator_group.google_rep.filter()]

        # if user.profile.team and user.profile.location:
        #     # print user.profile.team.team_name, user.profile.location.location_name
        #     if user.profile.team.team_name in teams and user.profile.location.location_name in locations:
        #         return operator_group.olark_script
        #     elif user.email in emails:
        #         return operator_group.olark_script
        # elif user.email in emails:
        #     return operator_group.olark_script

    if user.profile.team and user.profile.location:

        chat_group = OlarkChatGroup.objects.filter(programs__in=[user.profile.team], target_location__in=[user.profile.location])
        if len(chat_group) > 0:
            return chat_group[0].olark_script

        if user.email:
            chat_group = OlarkChatGroup.objects.filter(google_rep__in=[user])
            if len(chat_group) > 0:
                return chat_group[0].olark_script
            else:
                return ''

    elif user.email:
        chat_group = OlarkChatGroup.objects.filter(google_rep__in=[user])
        if len(chat_group) > 0:
            return chat_group[0].olark_script
        else:
            return ''


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
