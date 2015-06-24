from django.contrib import admin
from main.models import ContectList, CustomerTestimonials, UserDetails, Notification, Feedback, OlarkChatGroup
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse
from main.forms import OlarkChatGroupForm


class ContactAdmin(admin.ModelAdmin):
    list_display = ('position_type', 'first_name', 'last_name', 'email', 'phone_number', 'skype_id', 'profile_photo')
    filter_horizontal = ('target_location',)
admin.site.register(ContectList, ContactAdmin)


class CustomerTestimonialsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'statement_text')

admin.site.register(CustomerTestimonials, CustomerTestimonialsAdmin)


class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'user_supporting_region', 'user_manager_name',
                    'user_manager_email', 'phone', 'team', 'location', 'profile_photo_url')

    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'user__username']

admin.site.register(UserDetails, UserDetailsAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_visible', )

admin.site.register(Notification, NotificationAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'cid', 'advertiser_name', 'location', 'language', 'feedback_type', 'description', 'created_date')

admin.site.register(Feedback, FeedbackAdmin)


class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'

    readonly_fields = LogEntry._meta.get_all_field_names()

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')


admin.site.register(LogEntry, LogEntryAdmin)


class OlarkChatGroupAdmin(admin.ModelAdmin):
    form = OlarkChatGroupForm
    list_display = ('operator_group', 'program_list', 'location_list', 'rep_list',)
    filter_horizontal = ('programs', 'target_location', 'google_rep')

admin.site.register(OlarkChatGroup, OlarkChatGroupAdmin)
