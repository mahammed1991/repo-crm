from django.contrib import admin
from main.models import ContectList, CustomerTestimonials, UserDetails, Notification, Feedback, OlarkChatGroup, ResourceFAQ
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse
from main.forms import OlarkChatGroupForm
from lib.admin_helpers import CustomAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.encoding import smart_str

def export_csv(modeladmin, request, queryset):
    import csv
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=user_email.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional.Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"email"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.email),
        ])
    return response
export_csv.short_description = u"Export Users Emails"

class MyUserAdmin(UserAdmin):
    actions = [export_csv]
    UserAdmin.list_display = ('email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')
    readonly_fields = ['email', 'is_active', 'date_joined']

    def get_readonly_fields(self, request, obj=None):
        return CustomAdmin.get_readonly_status(request, self.readonly_fields, obj)

    def has_add_permission(self, request):
        return CustomAdmin.get_permission_status(request)

    def has_delete_permission(self, request, obj=None):
        return CustomAdmin.get_permission_status(request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = CustomAdmin.get_view_status(request, extra_context)
        return super(MyUserAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('position_type', 'first_name', 'last_name', 'email', 'phone_number', 'skype_id', 'profile_photo')
    filter_horizontal = ('target_location',)

    def has_add_permission(self, request):
        return CustomAdmin.get_permission_status(request)

    def has_delete_permission(self, request, obj=None):
        return CustomAdmin.get_permission_status(request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = CustomAdmin.get_view_status(request, extra_context)
        return super(ContactAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

admin.site.register(ContectList, ContactAdmin)


class CustomerTestimonialsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'statement_text')

admin.site.register(CustomerTestimonials, CustomerTestimonialsAdmin)


class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'user_supporting_region', 'user_manager_name',
                    'user_manager_email', 'phone', 'team', 'location', 'profile_photo_url')

    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'user__username']
    # readonly_fields = ['user', 'role', 'user_supporting_region', 'user_manager_name', 'user_manager_email', 'phone', 'team', 'location',
    #                    'profile_photo_url']

    # def get_readonly_fields(self, request, obj=None):
    #     return CustomAdmin.get_readonly_status(request, self.readonly_fields, obj)

    def has_add_permission(self, request):
        return CustomAdmin.get_permission_status(request)

    def has_delete_permission(self, request, obj=None):
        return CustomAdmin.get_permission_status(request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = CustomAdmin.get_view_status(request, extra_context)
        return super(UserDetailsAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)


admin.site.register(UserDetails, UserDetailsAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('text', 'region_list', 'location_list', 'is_visible',)
    filter_horizontal = ('target_location', 'region')

admin.site.register(Notification, NotificationAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'cid', 'advertiser_name', 'location', 'language', 'feedback_type', 'description', 'created_date')
    readonly_fields = ['user', 'title', 'cid', 'advertiser_name', 'location', 'language', 'feedback_type', 'description', 'created_date']

    def get_readonly_fields(self, request, obj=None):
        return CustomAdmin.get_readonly_status(request, self.readonly_fields, obj)

    def has_add_permission(self, request):
        return CustomAdmin.get_permission_status(request)

    def has_delete_permission(self, request, obj=None):
        return CustomAdmin.get_permission_status(request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = CustomAdmin.get_view_status(request, extra_context)
        return super(FeedbackAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

admin.site.register(Feedback, FeedbackAdmin)


class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'

    readonly_fields = LogEntry._meta.get_all_field_names()

    list_filter = [
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

    def get_readonly_fields(self, request, obj=None):
        return CustomAdmin.get_readonly_status(request, self.readonly_fields, obj)

    def has_add_permission(self, request):
        return CustomAdmin.get_permission_status(request)

    def has_delete_permission(self, request, obj=None):
        return CustomAdmin.get_permission_status(request)

admin.site.register(OlarkChatGroup, OlarkChatGroupAdmin)


class ResourceFAQAdmin(admin.ModelAdmin):

    list_display = ('submited_by', 'task_type', 'task_question')
    readonly_fields = ['submited_by', 'task_type', 'task_question']

    def get_readonly_fields(self, request, obj=None):
        return CustomAdmin.get_readonly_status(request, self.readonly_fields, obj)

    def has_add_permission(self, request):
        return CustomAdmin.get_permission_status(request)

    def has_delete_permission(self, request, obj=None):
        return CustomAdmin.get_permission_status(request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = CustomAdmin.get_view_status(request, extra_context)
        return super(ResourceFAQAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

admin.site.register(ResourceFAQ, ResourceFAQAdmin)
