import os
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from django.utils.translation import ugettext as _


# Create your models here.
class Leads(models.Model):
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

    dials = models.IntegerField(default=0)
    lead_sub_status = models.CharField(max_length=100, null=True)

    created_date = models.DateTimeField(default=datetime.utcnow())
    updated_date = models.DateTimeField(default=datetime.utcnow(), auto_now=True)

    sf_lead_id = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Leads"


class Timezone(models.Model):
    zone_name = models.CharField(max_length=20)
    time_value = models.CharField(max_length=6)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.zone_name

    class Meta:
        db_table = 'timezone'
        ordering = ['zone_name']


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

    location_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, null=True, default=None, blank=True)
    time_zone = models.ManyToManyField(Timezone)
    language = models.ManyToManyField(Language)
    flag_image = models.ImageField(upload_to=get_flag_image, null=True, max_length=100, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    def timezone_list(self):
        return ", ".join(["%s (UTC %s)" % (t.zone_name, t.time_value) for t in self.time_zone.all()])

    @property
    def flag_filename(self):
        return os.path.basename(self.flag_image.name)

    def clean(self):
        # Either email or google_id. Both cannot be empty.
        if self.location_name == '':
            raise ValidationError('Please enter location name.')

        image = self.flag_image

        if image:
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

    def __str__(self):              # __unicode__ on Python 2
        return self.location_name

    class Meta:
        db_table = 'locations'
        ordering = ['location_name']


class RegalixTeams(models.Model):
    team_name = models.CharField(max_length=100)
    location = models.ManyToManyField(Location)
    process_type = models.CharField(max_length=50, choices=(
        ('TAG', 'TAG'),
        ('MIGRATION', 'MIGRATION'),
        ('SHOPPING', 'SHOPPING'),
    ), default='TAG')

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    def location_list(self):
        return ", ".join(["%s" % (l.location_name) for l in self.location.all()])

    def __str__(self):              # __unicode__ on Python 2
        return self.team_name

    class Meta:
        db_table = 'regalix_teams'
        ordering = ['team_name']
        verbose_name_plural = "Regalix Teams"


class Team(models.Model):
    """ Team/Program information """
    team_name = models.CharField(max_length=100, unique=True)

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
    is_active = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'code_types'
        ordering = ['name']
        verbose_name_plural = "Code Types"


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
