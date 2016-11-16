import os
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.
class Leads(models.Model):
    # Lead Owner Details and Lead Information
    lead_owner_name = models.CharField(max_length=255, null=False)  # cannot be changed by REP
    lead_owner_email = models.CharField(max_length=255, null=False)

    # Google Manager Details
    google_rep_name = models.CharField(max_length=255)
    google_rep_email = models.CharField(max_length=255)
    google_rep_location = models.CharField(max_length=100, null=True, blank=True)
    google_rep_manager_email = models.CharField(max_length=100, null=True, blank=True)
    google_rep_manager_name = models.CharField(max_length=100, null=True, blank=True)
    team = models.CharField(max_length=100)

    # Advertiser Contact Details
    customer_id = models.CharField(max_length=50)
    company = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    first_name_optional = models.CharField(max_length=50)
    last_name_optional = models.CharField(max_length=100)
    phone_optional = models.CharField(max_length=100)
    email_optional = models.CharField(max_length=100)
    country = models.CharField(max_length=255)  # Advertaiser Location
    time_zone = models.CharField(max_length=75)
    language = models.CharField(max_length=50, blank=True, null=True)
    primary_contact_role = models.CharField(max_length=100, blank=True, null=True)
    webmaster_phone = models.CharField(max_length=255, blank=True, null=True)
    webmaster_name = models.CharField(max_length=255, blank=True, null=True)
    webmaster_email = models.CharField(max_length=255, blank=True, null=True)
    appointment_date = models.DateTimeField(blank=True, null=True)  # In advertaiser Timezone
    appointment_date_in_ist = models.DateTimeField(blank=True, null=True)
    rescheduled_appointment = models.DateTimeField(blank=True, null=True)
    rescheduled_appointment_in_ist = models.DateTimeField(blank=True, null=True)
    first_contacted_on = models.DateTimeField(blank=True, null=True)

    # Lead Processing information
    lead_status = models.CharField(max_length=50)
    lead_sub_status = models.CharField(max_length=100, null=True)
    ecommerce = models.IntegerField(default=0)
    date_of_installation = models.DateTimeField(blank=True, null=True)
    regalix_comment = models.TextField()
    google_comment = models.TextField()
    eto_ldap = models.CharField(max_length=100, blank=True, null=True, default='')
    tat = models.IntegerField(default=0)
    gcss = models.CharField(max_length=50, blank=True, null=True)

    # Automated??
    no_of_calls_inbound = models.CharField(max_length=150)
    no_of_calls_outbound = models.CharField(max_length=150)
    emails_sent = models.CharField(max_length=150)
    emails_received = models.CharField(max_length=150)
    call_recordings = models.CharField(max_length=150)
    email_logs = models.CharField(max_length=150)
    is_active = models.IntegerField(default=1)
    sf_lead_id = models.CharField(max_length=50, unique=True)
    dials = models.IntegerField(default=0)

    # Code 1 to 5
    code_1 = models.TextField()
    url_1 = models.CharField(max_length=255)
    type_1 = models.CharField(max_length=150)
    comment_1 = models.TextField()
    user_list_id_1 = models.CharField(max_length=100, blank=True, null=True, default='')
    rlsa_bid_adjustment_1 = models.CharField(max_length=100, blank=True, null=True, default='')
    internale_cid_1 = models.CharField(max_length=100, blank=True, null=True, default='')
    override_existing_bid_modifiers_1 = models.CharField(max_length=100, blank=True, null=True, default='')
    campaign_id_1 = models.CharField(max_length=100, blank=True, null=True, default='')

    code_2 = models.TextField()
    url_2 = models.CharField(max_length=255)
    type_2 = models.CharField(max_length=150)
    comment_2 = models.TextField()
    user_list_id_2 = models.CharField(max_length=100, blank=True, null=True, default='')
    rlsa_bid_adjustment_2 = models.CharField(max_length=100, blank=True, null=True, default='')
    internale_cid_2 = models.CharField(max_length=100, blank=True, null=True, default='')
    override_existing_bid_modifiers_2 = models.CharField(max_length=100, blank=True, null=True, default='')
    campaign_id_2 = models.CharField(max_length=100, blank=True, null=True, default='')

    code_3 = models.TextField()
    url_3 = models.CharField(max_length=255)
    type_3 = models.CharField(max_length=150)
    comment_3 = models.TextField()
    user_list_id_3 = models.CharField(max_length=100, blank=True, null=True, default='')
    rlsa_bid_adjustment_3 = models.CharField(max_length=100, blank=True, null=True, default='')
    internale_cid_3 = models.CharField(max_length=100, blank=True, null=True, default='')
    override_existing_bid_modifiers_3 = models.CharField(max_length=100, blank=True, null=True, default='')
    campaign_id_3 = models.CharField(max_length=100, blank=True, null=True, default='')

    code_4 = models.TextField()
    url_4 = models.CharField(max_length=255)
    type_4 = models.CharField(max_length=150)
    comment_4 = models.TextField()
    user_list_id_4 = models.CharField(max_length=100, blank=True, null=True, default='')
    rlsa_bid_adjustment_4 = models.CharField(max_length=100, blank=True, null=True, default='')
    internale_cid_4 = models.CharField(max_length=100, blank=True, null=True, default='')
    override_existing_bid_modifiers_4 = models.CharField(max_length=100, blank=True, null=True, default='')
    campaign_id_4 = models.CharField(max_length=100, blank=True, null=True, default='')

    code_5 = models.TextField()
    url_5 = models.CharField(max_length=255)
    type_5 = models.CharField(max_length=150)
    comment_5 = models.TextField()
    user_list_id_5 = models.CharField(max_length=100, blank=True, null=True, default='')
    rlsa_bid_adjustment_5 = models.CharField(max_length=100, blank=True, null=True, default='')
    internale_cid_5 = models.CharField(max_length=100, blank=True, null=True, default='')
    override_existing_bid_modifiers_5 = models.CharField(max_length=100, blank=True, null=True, default='')
    campaign_id_5 = models.CharField(max_length=100, blank=True, null=True, default='')

    # Project Argos
    feed_optimisation_status = models.CharField(max_length=300, blank=True, null=True)
    feed_optimisation_sub_status = models.CharField(max_length=300, blank=True, null=True)
    number_of_products = models.CharField(max_length=100, blank=True, null=True)
    additional_description = models.CharField(max_length=1000, blank=True, null=True)
    area_tobe_improved = models.CharField(max_length=1000, blank=True, null=True)
    shopping_feed_link = models.CharField(max_length=1000, blank=True, null=True)
    business_type = models.CharField(max_length=100, blank=True, null=True)
    authcase_id = models.CharField(max_length=100, blank=True, null=True)
    additional_support_beyond_case = models.CharField(max_length=1000, blank=True, null=True)

    # System Information
    created_date = models.DateTimeField(default=datetime.utcnow())
    updated_date = models.DateTimeField(default=datetime.utcnow(), auto_now=True)

    class Meta:
        verbose_name_plural = "Leads"

class TagLeadDetail(models.Model):
    lead_id = models.ForeignKey(Leads)
    # QC
    qc_on = models.DateTimeField(blank=True, null=True)
    qc_by = models.CharField(max_length=100, blank=True, null=True)
    qc_comments = models.TextField(blank=True, null=True)

    # New Mandatory Fields
    auth_email_sent = models.NullBooleanField(blank=True, null=True)
    live_transfer = models.CharField(max_length=100, blank=True, null=True, default='')
    cms_platform = models.CharField(max_length=80, blank=True, null=True, default='')
    appointment_sub_status = models.CharField(max_length=100, blank=True, null=True, default='')
    gcase_id = models.CharField(max_length=80, blank=True, null=True, default='')
    gcss_status = models.CharField(max_length=80, blank=True, null=True, default='')
    gcss_status_approved_by = models.CharField(max_length=100, blank=True, null=True, default='')
    mouse_control_taken = models.CharField(max_length=100, blank=True, null=True, default='')
    mouse_control_approved_by = models.CharField(max_length=100, blank=True, null=True, default='')
    list_type = models.CharField(max_length=100, blank=True, null=True, default='')
    regalix_sme = models.CharField(max_length=100, blank=True, null=True, default='')
    lead_difficulty_level = models.CharField(max_length=100, blank=True, null=True, default='')
    rlsa_tag_team_contacted = models.CharField(max_length=100, blank=True, null=True, default='')
    campaign_created_by_gsr = models.CharField(max_length=100, blank=True, null=True, default='')
    adwords_cid_submitted = models.CharField(max_length=100, blank=True, null=True, default='')

    # New Fields
    implemented_code_is = models.CharField(max_length=80, blank=True, null=True, default='')
    number_of_dails = models.IntegerField(default=0)
    pla_sub_status = models.CharField(max_length=80, blank=True, null=True, default='')
    dynamic_variable_set = models.CharField(max_length=100, blank=True, null=True, default='')
    dead_lead_date = models.DateTimeField(blank=True, null=True)
    last_contacted_on = models.DateTimeField(blank=True, null=True)
    is_backup_taken = models.NullBooleanField(blank=True, null=True)
    tag_via_gtm = models.NullBooleanField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    service_segment = models.CharField(max_length=100, blank=True, null=True, default='')
    rlsa_auth_approval = models.CharField(max_length=100, blank=True, null=True, default='')

    # Agency Details
    agency_poc = models.CharField(max_length=80, blank=True, null=True, default='')
    agency_name = models.CharField(max_length=100, blank=True, null=True, default='')
    agency_phone = models.CharField(max_length=80, blank=True, null=True, default='')
    agency_email = models.CharField(max_length=100, blank=True, null=True, default='')
    agency_bundle_number = models.CharField(max_length=100, blank=True, null=True, default='')
    agency_service_case_id = models.CharField(max_length=100, blank=True, null=True, default='')

    # New - Shopping Details
    mc_id = models.CharField(max_length=100, blank=True, null=True, default='')
    opt_in_percent = models.CharField(max_length=100, blank=True, null=True, default='')
    client_web_inventory = models.CharField(max_length=100, blank=True, null=True, default='')
    recommended_bid = models.CharField(max_length=100, blank=True, null=True, default='')
    recommended_budget= models.CharField(max_length=100, blank=True, null=True, default='')
    sqo_sto_comments = models.CharField(max_length=1000, blank=True, null=True, default='')
    secured_checkout = models.CharField(max_length=100, blank=True, null=True, default='')
    payment_gateway = models.CharField(max_length=100, blank=True, null=True, default='')
    recommended_mobile_bid_modifier = models.CharField(max_length=100, blank=True, null=True, default='')
    shopping_polices_verified = models.NullBooleanField(blank=True, null=True)
    type_of_policy_violation = models.CharField(max_length=100, blank=True, null=True, default='')
    shopping_troubleshoot_issue_type = models.CharField(max_length=100, blank=True, null=True, default='')
    products_uploaded = models.CharField(max_length=100, blank=True, null=True, default='')
    campaign_id = models.CharField(max_length=100, blank=True, null=True, default='')
    feed_upload_method = models.CharField(max_length=100, blank=True, null=True, default='')

# Create your models here.
class WPPLeads(models.Model):
    # ref_google_rep_user = models.ForeignKey(User)
    google_rep_name = models.CharField(max_length=255)
    google_rep_email = models.CharField(max_length=255)

    ecommerce = models.IntegerField(default=0)
    lead_owner_name = models.CharField(max_length=255, null=False)
    lead_owner_email = models.CharField(max_length=255, null=False)
    company = models.CharField(max_length=255)
    lead_status = models.CharField(max_length=50)
    country = models.CharField(max_length=255)

    customer_id = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    first_name_optional = models.CharField(max_length=50)
    last_name_optional = models.CharField(max_length=100)
    phone_optional = models.CharField(max_length=100)
    email_optional = models.CharField(max_length=100)

    date_of_installation = models.DateTimeField(blank=True, null=True)

    time_zone = models.CharField(max_length=75)

    regalix_comment = models.TextField()
    google_comment = models.TextField()

    code_1 = models.TextField()
    url_1 = models.CharField(max_length=255)
    type_1 = models.CharField(max_length=150)
    comment_1 = models.TextField()

    code_2 = models.TextField()
    url_2 = models.CharField(max_length=255)
    type_2 = models.CharField(max_length=150)
    comment_2 = models.TextField()

    code_3 = models.TextField()
    url_3 = models.CharField(max_length=255)
    type_3 = models.CharField(max_length=150)
    comment_3 = models.TextField()

    code_4 = models.TextField()
    url_4 = models.CharField(max_length=255)
    type_4 = models.CharField(max_length=150)
    comment_4 = models.TextField()

    code_5 = models.TextField()
    url_5 = models.CharField(max_length=255)
    type_5 = models.CharField(max_length=150)
    comment_5 = models.TextField()

    no_of_calls_inbound = models.CharField(max_length=150)
    no_of_calls_outbound = models.CharField(max_length=150)
    emails_sent = models.CharField(max_length=150)
    emails_received = models.CharField(max_length=150)
    call_recordings = models.CharField(max_length=150)
    email_logs = models.CharField(max_length=150)
    team = models.CharField(max_length=100)
    is_active = models.IntegerField(default=1)

    appointment_date = models.DateTimeField(blank=True, null=True)
    first_contacted_on = models.DateTimeField(blank=True, null=True)

    # Rescheduled Appointments
    rescheduled_appointment = models.DateTimeField(blank=True, null=True)
    rescheduled_appointment_in_ist = models.DateTimeField(blank=True, null=True)

    dials = models.IntegerField(default=0)
    lead_sub_status = models.CharField(max_length=100, null=True)

    tat = models.IntegerField(default=0)

    created_date = models.DateTimeField(default=datetime.utcnow())
    updated_date = models.DateTimeField(default=datetime.utcnow(), auto_now=True)

    sf_lead_id = models.CharField(max_length=50, unique=True)
    treatment_type = models.CharField(max_length=100, blank=True, null=True)
    additional_notes = models.TextField(default='')
    mockup_url = models.CharField(max_length=255, null=True)
    mockup_password = models.CharField(max_length=255, null=True)
    stage_url = models.CharField(max_length=255, null=True)
    stage_password = models.CharField(max_length=255, null=True)
    is_ab_test = models.CharField(max_length=255, null=True, default='YES')
    is_nominated = models.BooleanField(default=False)
    ref_uuid = models.CharField(max_length=100, blank=True, null=True)

    is_build_eligible = models.CharField(max_length=10, blank=True, null=True)

    # CRM fields
    actual_deployment_date = models.DateTimeField(blank=True, null=True)
    actual_mock_review_date = models.DateTimeField(blank=True, null=True)
    actual_stage_review_date = models.DateTimeField(blank=True, null=True)
    actual_ui_ux_date = models.DateTimeField(blank=True, null=True)
    additional_notes_if_any = models.TextField(blank=True, null=True)
    advertiser_email_3 = models.CharField(max_length=80, blank=True, null=True)
    advertiser_role  = models.TextField(blank=True, null=True)
    advertisers_e_mail_wpp = models.CharField(max_length=80, blank=True, null=True)
    advertiser_telephone_3 = models.CharField(max_length=40, blank=True, null=True)
    adwords_account_status = models.CharField(max_length=50, blank=True, null=True)
    conversion_goal = models.TextField(blank=True, null=True)
    dead_lead_date = models.DateTimeField(blank=True, null=True)
    delivery_pod = models.CharField(max_length=50, blank=True, null=True)
    design_effort = models.FloatField(blank=True, null=True) 
    design_owner = models.CharField(max_length=50, blank=True, null=True)
    dev_owner = models.CharField(max_length=50, blank=True, null=True)
    development_effort = models.FloatField(blank=True, null=True) 
    email_mandatory = models.CharField(max_length=80, blank=True, null=True)
    engagement_effort = models.CharField(max_length=80, blank=True, null=True)
    first_name_3 = models.CharField(max_length=50, blank=True, null=True)
    google_account_manager = models.CharField(max_length=50, blank=True, null=True)
    invision_links = models.TextField(blank=True, null=True)
    appointment_time_in_ist = models.DateTimeField(blank=True, null=True) 
    last_name_3 = models.CharField(max_length=50, blank=True, null=True)
    lead_source_c = models.CharField(max_length=50, blank=True, null=True)
    lead_via_live_transfer = models.CharField(max_length=50, blank=True, null=True)
    lead_source = models.CharField(max_length=50, blank=True, null=True)
    advertiser_location = models.CharField(max_length=80, blank=True, null=True)
    no_of_pages = models.FloatField(blank=True, null=True)
    planned_deployment_date = models.DateTimeField(blank=True, null=True)
    planned_stage_review_date = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=80, blank=True, null=True)
    qa_owner = models.CharField(max_length=80, blank=True, null=True)
    reschedule_email_schedule_time = models.DateTimeField(blank=True, null=True) 
    role_2 = models.TextField(blank=True, null=True)
    role_3 = models.TextField(blank=True, null=True)
    role_others1 = models.TextField(blank=True, null=True)
    role_others2 = models.TextField(blank=True, null=True)
    role_others = models.TextField(blank=True, null=True)
    technology = models.CharField(max_length=80, blank=True, null=True)
    testing_effort = models.FloatField(blank=True, null=True) 
    tracking_codes = models.TextField(blank=True, null=True)
    screenshare_scheduled = models.CharField(max_length=80, blank=True, null=True)
    why_deferred = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "WPP Leads"


class Timezone(models.Model):
    zone_name = models.CharField(max_length=20, unique=True)
    time_value = models.CharField(max_length=6)

    is_active = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    # Validate fields
    def clean(self):
        # Time zone value format should be Ex: +0:00 or -0:00.
        if self.time_value == '':
            raise ValidationError('Please enter Timezone value.')

        if "+" not in self.time_value:
            if "-" not in self.time_value:
                raise ValidationError('Timezone value format shoud be starts with + or - symbol.')

        if ":" not in self.time_value:
            raise ValidationError('Timezone value format shoud be +hh:mm or -hh:mm')

        if len(self.time_value.split(":")) > 2:
            raise ValidationError('value should be hh:mm formate.')

        if len(self.time_value.split(":")) == 2:
            hh = self.time_value.split(":")[0]
            mm = self.time_value.split(":")[1]
            if hh[0] not in ['+', '-']:
                raise ValidationError('In timezone value + or - symbol should be first character')

            if len(hh[1:]) == 0:
                raise ValidationError('Please enter hours')

            if len(mm) == 0:
                raise ValidationError('Please enter minutes')

            try:
                hh = int(hh[1:])
                if hh > 13:
                    raise ValidationError('Hours should be less than 14')
            except Exception:
                raise ValidationError('Hours should be in numeric and less than 14')

            try:
                mm = int(mm)
                if mm > 59:
                    raise ValidationError('Minutes should be less than 60')
            except Exception:
                raise ValidationError('Minutes should be in numeric and less than 60')

    def __str__(self):              # __unicode__ on Python 2
        return self.zone_name

    class Meta:
        db_table = 'timezone'
        ordering = ['zone_name']


class TimezoneMapping(models.Model):
    standard_timezone = models.ForeignKey(Timezone, related_name="std_timezone", unique=True)
    daylight_timezone = models.ForeignKey(Timezone, related_name="ds_timezone", unique=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        db_table = 'timezone_mapping'
        ordering = ['standard_timezone']
        unique_together = ('standard_timezone', 'daylight_timezone')
        verbose_name_plural = "Timezone Mapping"


class Language(models.Model):
    """ Language model """

    language_name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __str__(self):
        return self.language_name

    class Meta:
        db_table = 'languages'
        verbose_name_plural = 'Languages'


class Location(models.Model):

    def get_flag_image(instance, flag_filename):
        """ Dynamic location flag image path """

        ext = flag_filename.split('.')[-1]

        if instance.location_name:
            filename = "%s.%s" % (instance.location_name.replace(' ', '-'), ext)
        else:
            filename = flag_filename
        return os.path.join('country_flag/', filename)

    location_name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=50, null=True, default=None, blank=True)
    time_zone = models.ManyToManyField(Timezone, related_name="standard_timezone", limit_choices_to={'is_active': True})
    ds_time_zone = models.ManyToManyField(Timezone, related_name="daylight_timezone", blank=True, null=True, limit_choices_to={'is_active': True})
    daylight_start = models.DateTimeField(blank=True, null=True, default=None)
    daylight_end = models.DateTimeField(blank=True, null=True, default=None)
    primary_language = models.ForeignKey(Language, related_name="primary_language", null=False, blank=False, default=1)
    language = models.ManyToManyField(Language)
    flag_image = models.ImageField(upload_to=get_flag_image, null=True, max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    def timezone_list(self):
        return ", ".join(["%s (UTC %s)" % (t.zone_name, t.time_value) for t in self.time_zone.all()])

    def ds_timezone_list(self):
        return ", ".join(["%s (UTC %s)" % (t.zone_name, t.time_value) for t in self.ds_time_zone.all()])

    def secondary_language_list(self):
        return ", ".join(["%s" % (l.language_name) for l in self.language.all()])

    @property
    def flag_filename(self):
        return os.path.basename(self.flag_image.name)

    def clean(self):
        # Either email or google_id. Both cannot be empty.
        if self.location_name == '':
            raise ValidationError('Please enter location name.')

        if self.daylight_start or self.daylight_end:
            if not self.daylight_start:
                raise ValidationError('Please enter daylight start date.')
            if not self.daylight_end:
                raise ValidationError('Please enter daylight end date.')
            elif self.daylight_start >= self.daylight_end:
                raise ValidationError('Daylight start date should be less than daylight end date.')

        image = self.flag_image
        if image:
            try:
                img = Image.open(image)

                w, h = img.size

                # validate dimensions
                max_width = 200
                max_height = 200
                if w > max_width or h > max_height:
                    raise ValidationError(
                        _('Please use an image that is smaller or equal to '
                          '%s x %s pixels.' % (max_width, max_height)))

                # validate content type
                img_ext = image.name.split('.')[1]
                if img_ext not in ['png']:
                    raise ValidationError(_('Image is not in PNG format. Please use a PNG image.'))

                return image
            except Exception:
                if self.flag_filename:
                    if not os.path.isfile(os.path.join('country_flag/', self.flag_filename)):
                        self.flag_image.delete()
                        return image

    def __str__(self):              # __unicode__ on Python 2
        return self.location_name

    class Meta:
        db_table = 'locations'
        ordering = ['location_name']
        verbose_name_plural = 'Target Location'


class PicassoLeadGroupType(models.Model):
   group_type = models.CharField(max_length=100, blank=True, null=True)
   is_active = models.BooleanField(default=True)

   def __str__(self):
       return self.group_type


class Team(models.Model):
    """ Team/Program information """
    picasso_lead_group_type = models.ForeignKey(PicassoLeadGroupType,blank=True,null=True,default=None)
    team_name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    belongs_to = models.CharField(max_length=50, blank=False, choices=(
        ('TAG', 'TAG'),
        ('WPP', 'WPP'),
        ('PICASSO', 'PICASSO'),
        ('TAG-WPP', 'TAG-WPP'),
        ('TAG-PICASSO', 'TAG-PICASSO'),
        ('WPP-PICASSO', 'WPP-PICASSO'),
        ('ALL', 'ALL')), default='TAG'
    )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __str__(self):
        return self.team_name

    class Meta:
        db_table = 'teams'
        ordering = ['team_name']
        verbose_name_plural = "Programs"


class CodeType(models.Model):
    """ Code Types list """

    name = models.CharField(max_length=100, unique=True)
    avg_setup_time = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'code_types'
        ordering = ['name']
        verbose_name_plural = "Code Types"


class RegalixTeams(models.Model):

    def default_team_lead(self):
        try:
            lead_owner = User.objects.get(email=settings.DEFAULT_LEAD_OWNER_EMAIL)
        except ObjectDoesNotExist:
            lead_owner = User.objects.create(
                email=settings.DEFAULT_LEAD_OWNER_EMAIL,
                username=settings.DEFAULT_LEAD_OWNER_EMAIL,
                first_name=settings.DEFAULT_LEAD_OWNER_FNAME,
                last_name=settings.DEFAULT_LEAD_OWNER_LNAME
            )
        return lead_owner

    team_name = models.CharField(max_length=100, unique=True)
    location = models.ManyToManyField(Location, limit_choices_to={'is_active': True})
    program = models.ManyToManyField(Team, blank=True, null=True, limit_choices_to={'is_active': True})
    ldap = models.ManyToManyField(User, blank=True, null=True, related_name="ldap")
    process_type = models.CharField(max_length=50, blank=False, choices=(
        ('TAG', 'TAG'),
        ('SHOPPING', 'SHOPPING'),
        ('WPP', 'WPP'),
        ('MIGRATION', 'MIGRATION'),)
    )
    team_lead = models.ManyToManyField(User, related_name="team_lead")
    team_manager = models.ManyToManyField(User, related_name="team_manager")
    is_active = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    def location_list(self):
        return ", ".join(["%s" % (l.location_name) for l in self.location.all()])

    def team_lead_list(self):
        return ", ".join(["%s %s" % (usr.first_name, usr.last_name) for usr in self.team_lead.all()])

    def team_manager_list(self):
        return ", ".join(["%s %s" % (usr.first_name, usr.last_name) for usr in self.team_manager.all()])

    def __str__(self):              # __unicode__ on Python 2
        return self.team_name

    class Meta:
        db_table = 'regalix_teams'
        ordering = ['team_name']
        verbose_name_plural = "Regalix Teams"


class ChatMessage(models.Model):
    """ Chat Message Model """

    lead = models.ForeignKey(Leads, null=False)
    user_id = models.CharField(max_length=255, null=False)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'chat_message'
        verbose_name_plural = 'Chat Message'


class AgencyDetails(models.Model):
    """ Agency Details """

    google_rep = models.ForeignKey(User)
    agency_name = models.CharField(max_length=255, null=False)
    location = models.ForeignKey(Location, null=False)
    timezone = models.ForeignKey(Timezone, null=False)
    language = models.ForeignKey(Language, null=True, blank=True)
    appointment_date = models.DateTimeField(default=datetime.utcnow())

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        db_table = 'agency_details'
        verbose_name_plural = 'Agency Details'


class ContactPerson(models.Model):
    """ Contact Persons """

    contact_person = models.CharField(max_length=255, null=False)
    contact_email = models.EmailField(max_length=255, null=False, unique=True)
    contact_phone = models.CharField(max_length=255, null=False)
    agency = models.ForeignKey(AgencyDetails)
    person_id = models.CharField(max_length=255, null=False)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        db_table = 'contact_person'
        verbose_name_plural = 'Contact Person'


class LeadForm(models.Model):
    """ Lead Form Names """
    name = models.CharField(max_length=255, null=False, unique=True)
    is_active = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'lead_forms'
        verbose_name_plural = 'Lead Forms'


class LeadFormAccessControl(models.Model):
    """ Lead Form Access Control """

    lead_form = models.ForeignKey(LeadForm, unique=True)
    programs = models.ManyToManyField(Team, blank=True, null=True)
    target_location = models.ManyToManyField(Location, blank=True, null=True)
    google_rep = models.ManyToManyField(User, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    def program_list(self):
        return ", ".join(["%s" % (p.team_name) for p in self.programs.all()])

    def location_list(self):
        return ", ".join(["%s" % (l.location_name) for l in self.target_location.all()])

    def rep_list(self):
        return ", ".join(["%s" % (r.get_full_name()) for r in self.google_rep.all()])

    # def __str__(self):
    #     return self.lead_form

    class Meta:
        db_table = 'lead_form_controls'
        verbose_name_plural = 'Lead Form Access Controls'


class SfdcUsers(models.Model):
    """ SFDC Users List """

    user_id = models.CharField(max_length=255, null=False)
    full_name = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=255, null=False)
    username = models.CharField(max_length=255, null=False)
    process_type = models.CharField(max_length=50, blank=True, choices=(
        ('TAG', 'TAG'),
        ('SHOPPING', 'SHOPPING'),
        ('RLSA', 'RLSA'),
        ('WPP', 'WPP'),
        ('Picasso Audits', 'Picasso Audits'),
        ('Shopping Argos','Shopping Argos')))
    shift_start = models.TimeField(blank=True, null=True)
    shift_end = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        db_table = 'sfdc_users'
        verbose_name_plural = 'SFDC Users'


class TreatmentType(models.Model):
    """ Treatment Type List """

    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'treatment_type'
        ordering = ['name']
        verbose_name_plural = "Treatment Types"


class PicassoLeads(models.Model):
    google_rep_name = models.CharField(max_length=255)
    google_rep_email = models.CharField(max_length=255)

    lead_owner_name = models.CharField(max_length=255, null=False)
    lead_owner_email = models.CharField(max_length=255, null=False)
    company = models.CharField(max_length=255)
    lead_status = models.CharField(max_length=50)
    country = models.CharField(max_length=255)

    customer_id = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    date_of_installation = models.DateTimeField(blank=True, null=True)

    regalix_comment = models.TextField()
    google_comment = models.TextField()

    code_1 = models.TextField()
    url_1 = models.CharField(max_length=255)
    type_1 = models.CharField(max_length=150)
    comment_1 = models.TextField()

    team = models.CharField(max_length=100)
    is_active = models.IntegerField(default=1)

    tat = models.IntegerField(default=0)

    created_date = models.DateTimeField(default=datetime.utcnow())
    updated_date = models.DateTimeField(default=datetime.utcnow(), auto_now=True)

    sf_lead_id = models.CharField(max_length=50, unique=True)
    additional_notes = models.TextField(default='')
    picasso_objective = models.CharField(max_length=255, null=True, blank=True)
    internal_cid = models.CharField(max_length=50, null=True)
    pod_name = models.CharField(max_length=50)
    treatment_type = models.CharField(max_length=100, blank=True, null=True)
    is_build_eligible = models.BooleanField(default=False)
    ref_uuid = models.CharField(max_length=100, blank=True, null=True)
    estimated_tat = models.DateTimeField(blank=True, null=True)
    crop_email = models.CharField(max_length=100, default='')
    my_advitiser_email = models.CharField(max_length=100, default='', blank=True, null=True)
    my_cases_alias = models.CharField(max_length=100, default='', blank=True, null=True)
    market_selector = models.CharField(max_length=100, default='', blank=True, null=True)
    language_selector = models.CharField(max_length=100, default='', blank=True, null=True)
    picasso_type = models.CharField(max_length=100, default='PICASSO', blank=True, null=True)

    # CRM fields
    approximate_tat = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    case_categoriser = models.CharField(max_length=50, blank=True, null=True)
    case_categorizer_notes = models.TextField(blank=True, null=True)
    case_notes_for_designer = models.TextField(blank=True, null=True)
    case_type = models.CharField(max_length=50, blank=True, null=True)
    design_completion_date = models.DateTimeField(blank=True, null=True)
    designer = models.CharField(max_length=50, blank=True, null=True)
    designer_email = models.CharField(max_length=50, blank=True, null=True)
    desktop_score = models.FloatField(blank=True, null=True)
    gcases_id = models.CharField(max_length=50, blank=True, null=True)
    gdrive_link = models.CharField(max_length=100, blank=True, null=True)
    googler_cases_alias = models.CharField(max_length=80, blank=True, null=True)
    googler_corporate_email = models.CharField(max_length=80, blank=True, null=True)
    invision_link = models.CharField(max_length=80, blank=True, null=True)
    invision_password = models.CharField(max_length=80, blank=True, null=True)
    link_to_mocks_drive_internal = models.CharField(max_length=200, blank=True, null=True)
    no_of_mocks_delivered = models.FloatField(blank=True, null=True)
    picasso_lead_age_days = models.FloatField(blank=True, null=True)
    picasso_lead_source = models.CharField(max_length=80, blank=True, null=True)
    picasso_lead_stage = models.CharField(max_length=80, blank=True, null=True)
    picasso_market_served = models.TextField(blank=True, null=True)
    picasso_program_categorization = models.TextField(blank=True, null=True)
    picasso_reference_id = models.TextField(blank=True, null=True)
    email_p = models.CharField(max_length=80, blank=True, null=True)
    speed_score = models.FloatField(blank=True, null=True)
    standardised_template_link = models.CharField(max_length=100, blank=True, null=True)
    url_2 = models.CharField(max_length=100, blank=True, null=True)
    url_3 = models.CharField(max_length=100, blank=True, null=True)
    user_experience_score = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Picasso Leads"


class BlackListedCID(models.Model):
    cid = models.CharField(max_length=50, unique=True)
    active = models.BooleanField(default=True)
    modified_by = models.ForeignKey(User, related_name='modified_by_user',default='', blank=True, null=True)
    created_date = models.DateTimeField(default=datetime.utcnow())
    modified_date = models.DateTimeField(default=datetime.utcnow(), auto_now=True)


# New feature for builds similar to Picasso Bolt
class BuildsBoltEligibility(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    cid = models.CharField(max_length=20)
    url = models.CharField(max_length=500, blank=True, null=True)
    domain = models.CharField(max_length=150, blank=True, null=True)
    bolt_eligible = models.BooleanField(default=True)
    last_assessed_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'builds_bolt_eligibility'
        verbose_name_plural = 'Builds Bolt Eligibility'


class WhiteListedAuditCID(models.Model):
    external_customer_id = models.CharField(max_length=50, unique=True)
    opportunity_type = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=datetime.utcnow())
    modified_date = models.DateTimeField(default=datetime.utcnow(), auto_now=True)


class ArgosProcessTimeTracker(models.Model):
    lid = models.ForeignKey(Leads)
    assignee = models.ForeignKey(User, related_name="assignee", default='', blank=True, null=True)
    products_count = models.IntegerField()
    attributes = models.TextField(blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    paused_on = models.DateTimeField(blank=True, null=True)
    resumed_on = models.DateTimeField(blank=True, null=True)
    time_spent = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=10, default="Start")  # Start, Started, Paused, Completed
    assigner = models.ForeignKey(User, related_name="assigner", default='', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)


class LeadHistory(models.Model):
    lead_id = models.IntegerField(default=0)
    modified_by = models.CharField(max_length=255)
    action_type = models.CharField(max_length=255) #OwnerChange, edited, image,imagelink 
    modifications = models.TextField() # json encoded old values [{field_name: field_value_old}]
    image_guid = models.CharField(max_length=255,blank=True, null=True)
    original_image_name = models.CharField(max_length=255,blank=True, null=True)
    image_link = models.CharField(max_length=600,blank=True, null=True)
    previous_owner = models.CharField(max_length=255,blank=True, null=True)
    current_owner = models.CharField(max_length=255,blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)