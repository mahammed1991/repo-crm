""" Admin related custome helpers """
from django.db.models import Q
from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row


class CustomAdmin(object):

    @staticmethod
    def get_permission_status(request):
        user_groups = request.user.groups.filter(Q(name='SUPERUSER') | Q(name='OPERATIONS'))
        if not user_groups:
            return False
        else:
            return True

    @staticmethod
    def get_readonly_status(request, readonly_fields, obj):
        user_groups = request.user.groups.filter(Q(name='SUPERUSER') | Q(name='OPERATIONS'))
        if not user_groups:
            return list(readonly_fields) + [field.name for field in obj._meta.fields]
        else:
            return list(readonly_fields)

    @staticmethod
    def get_view_status(request, extra_context):
        user_groups = request.user.groups.filter(Q(name='SUPERUSER') | Q(name='OPERATIONS'))
        if not user_groups:
            extra_context = extra_context or {}
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False
            return extra_context
        else:
            extra_context = extra_context or {}
            extra_context['show_save_and_continue'] = True
            extra_context['show_save'] = True
            return extra_context


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    ctx = original_submit_row(context)
    ctx.update({
        'show_save_and_add_another': context.get('show_save_and_add_another', ctx['show_save_and_add_another']),
        'show_save_and_continue': context.get('show_save_and_continue', ctx['show_save_and_continue']),
        'show_save': context.get('show_save', ctx['show_save'])})
    return ctx
