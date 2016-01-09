import os
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from datetime import datetime
from PIL import Image
from django.utils.translation import ugettext as _


from leads.models import Location, Team, Leads, TreatmentType
from reports.models import Region
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives


class Feedback(models.Model):
    """ Feedback data """

    def get_file_path(instance, filename):
        """ Dynamic file path """
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid4(), ext)
        return os.path.join('feedback/', filename)

    def default_lead_owner():
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

    user = models.ForeignKey(User, related_name='feedback_by')

    title = models.CharField(max_length=255)
    cid = models.CharField(max_length=150)
    advertiser_name = models.CharField(max_length=150)
    location = models.ForeignKey(Location)
    language = models.CharField(max_length=150)
    feedback_type = models.CharField(max_length=150)
    description = models.TextField()
    status = models.CharField(max_length=20, default='NEW')
    lead_owner = models.ForeignKey(User, related_name='lead_owner', default=default_lead_owner)
    google_account_manager = models.ForeignKey(User, related_name='google_account_manager', default=default_lead_owner)
    program = models.ForeignKey(Team, default=None, null=True)
    code_type = models.CharField(max_length=150, null=True, blank=True)

    attachment = models.FileField(upload_to=get_file_path)

    resolved_by = models.ForeignKey(User, related_name='resolved_by', null=True)
    resolved_date = models.DateTimeField(blank=True, null=True)

    second_resolved_by = models.ForeignKey(User, related_name='second_resolved_by', null=True)
    second_resolved_date = models.DateTimeField(blank=True, null=True)

    third_resolved_by = models.ForeignKey(User, related_name='third_resolved_by', null=True)
    third_resolved_date = models.DateTimeField(blank=True, null=True)
    sf_lead_id = models.CharField(max_length=50, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        return os.path.basename(self.attachment.name)

    class Meta:
        db_table = 'feedback'


class FeedbackComment(models.Model):
    """ Feedback comments """
    feedback = models.ForeignKey(Feedback)
    comment = models.TextField()
    comment_by = models.ForeignKey(User)
    feedback_status = models.CharField(max_length=20, default='NEW')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback_comments'
        ordering = ['-created_date']


class UserDetails(models.Model):
    """ Users additional information """
    user = models.OneToOneField(User, related_name='profile')

    role = models.IntegerField(default=settings.REGALIX_DEFAULT_ROLE, null=False)
    user_supporting_region = models.CharField(max_length=100)
    user_manager_name = models.CharField(max_length=100)
    user_manager_email = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    team = models.ForeignKey(Team, blank=True, null=True, default=None)
    location = models.ForeignKey(Location, blank=True, null=True, default=None)
    rep_location = models.CharField(max_length=255, default=None, blank=True, null=True)
    region = models.ForeignKey(Region, blank=True, null=True, default=None)
    profile_photo_url = models.CharField(max_length=255, default=None, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        verbose_name_plural = 'User Details'


class ContectList(models.Model):
    """ Contect List information """

    def get_profile_photo(instance, profile_photo_filename):
        """ Dynamic profile photo path """
        ext = profile_photo_filename.split('.')[-1]
        if instance.google_id:
            filename = "%s.%s" % (instance.google_id.split('@')[0], ext)
        elif instance.email:
            filename = "%s.%s" % (instance.email.split('@')[0], ext)
        else:
            filename = profile_photo_filename
        return os.path.join('profile_photo/', filename)

    position_type = models.CharField(max_length=100, blank=False, choices=(
        ('MANAGEMENT', 'MANAGEMENT'),
        ('OPERATIONS', 'OPERATIONS'),
        ('QUALITY', 'QUALITY'),
        ('TECH/SME', 'TECH/SME'),
        ('TAG', 'TAG'),
        ('SHOPPING', 'SHOPPING'),
        ('POD', 'POD'),
        ('MIS', 'MIS'),
        ('DESIGN/DEV', 'DESIGN/DEV'),)
    )
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True)
    google_id = models.EmailField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    skype_id = models.CharField(max_length=100, blank=True, null=True)
    target_location = models.ManyToManyField(Location, blank=True, null=True)
    profile_photo = models.ImageField(upload_to=get_profile_photo, blank=True, max_length=100)
    extn = models.CharField(max_length=100, blank=True, null=True)
    supporting_hours = models.CharField(max_length=100, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True, default=datetime.utcnow())
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True, default=datetime.utcnow())

    @property
    def profile_photo_filename(self):
        return os.path.basename(self.profile_photo.name)

    @property
    def profile_email_id(self):
        return self.email

    def clean(self):
        # Either email or google_id. Both cannot be empty.
        if self.email == '' and self.google_id == '':
            raise ValidationError('Both email and google_id cannot be empty. Please enter either your regalix email id or google email id.')

        image = self.profile_photo

        if image:
            try:
                img = Image.open(image)
            except Exception as e:
                print e
                raise ValidationError('Profile photo doesnot exist on the path, please clear the photo or upload a new profile photo.')
            w, h = img.size

            # validate dimensions
            max_width = 500
            max_height = 550
            if w > max_width or h > max_height:
                raise ValidationError(
                    _('Please use an image that is smaller or equal to '
                      '%s x %s pixels.' % (max_width, max_height)))

            # validate content type
            img_ext = image.name.split('.')[1]
            if img_ext not in ['png']:
                raise ValidationError(_('Image is not in PNG format. Please use a PNG image.'))

        return image

    class Meta:
        db_table = 'contact_list'
        ordering = ['first_name']
        verbose_name_plural = 'Contact List'


class CustomerTestimonials(models.Model):
    """ Customer Testimonials information """

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    statement_text = models.TextField(blank=False)
    email = models.EmailField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    customer_id = models.CharField(max_length=50, blank=True, null=True)
    sf_lead_id = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(default=datetime.utcnow())
    updated_date = models.DateTimeField(auto_now=True)

    def clean(self):
        # Either email or google_id. Both cannot be empty.
        raise_error = False
        if self.customer_id:
            leads = Leads.objects.filter(customer_id=self.customer_id)
            if leads and len(leads) > 1:
                if self.sf_lead_id:
                    leads = Leads.objects.filter(sf_lead_id=self.sf_lead_id)
                    if not leads:
                        raise_error = True
                else:
                    raise_error = True
        if raise_error:
            raise ValidationError('We found multiple leads on this customer ID!, please enter a valid SFDC lead id on Sf lead id field ')

    class Meta:
        db_table = 'customer_testimonials'
        ordering = ['-created_date']

    # Overriding
    def save(self, *args, **kwargs):
        super(CustomerTestimonials, self).save(*args, **kwargs)
        # Send Mails to google rep and their manager
        if self.sf_lead_id:
            lead = Leads.objects.filter(sf_lead_id=self.sf_lead_id)
            if lead:
                send_testimonial_notification(lead[0], self)
        else:
            lead = Leads.objects.filter(customer_id=self.customer_id)
            if lead:
                if len(lead) > 1:
                    pass
                else:
                    send_testimonial_notification(lead[0], self)


class Notification(models.Model):
    """ Notification information """

    text = models.TextField(blank=False)

    region = models.ManyToManyField(Region, blank=True, null=True)
    target_location = models.ManyToManyField(Location, blank=True, null=True)
    is_visible = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    def region_list(self):
        return ", ".join(["%s" % (r.name) for r in self.region.all()])

    def location_list(self):
        return ", ".join(["%s" % (l.location_name) for l in self.target_location.all()])

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_date']


class PortalFeedback(models.Model):
    """ Portal Feedback data """

    def get_file_path(instance, filename):
        """ Dynamic file path """
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid4(), ext)
        return os.path.join('feedback/', filename)

    user = models.ForeignKey(User, related_name='portal_feedback_by')
    feedback_type = models.CharField(max_length=150)
    description = models.TextField()
    attachment = models.FileField(upload_to=get_file_path)
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        return os.path.basename(self.attachment.name)

    class Meta:
        db_table = 'portal_feedback'


def send_testimonial_notification(lead, testimonial):
    """ Email Testimonial details to Google reps """

    mail_subject = "Customer Testimonial"
    mail_body = get_template('main/email/testimonial_feedback_mail.html').render(
        Context({
            'testimonial': testimonial,
            'site_url': 'gtrack.regalix.com',
            'google_rep_name': lead.google_rep_name,
        })
    )

    # get feedback user manager and lead owner managers information
    bcc = set([settings.BCC_EMAIL])

    mail_to = set([
        lead.google_rep_email if lead.google_rep_email else '',
        lead.lead_owner_email if lead.lead_owner_email else '',
        'g-crew@regalix-inc.com',
        'rwieker@google.com',
        'tkhan@regalix-inc.com',
        'sabinaa@google.com',
        'analytics.support@regalix-inc.com'
    ])

    mail_from = ''

    attachments = list()

    if settings.SFDC == 'STAGE':
        mail_subject = 'STAGE - ' + mail_subject
        mail_to = set()

    email = EmailMultiAlternatives(mail_subject, mail_body, mail_from, mail_to, list(bcc))
    email.attach_alternative(mail_body, "text/html")

    for attachment in attachments:
        email.attach(
            attachment.name,
            attachment.read()
        )
    try:
        email.send()
    except Exception, e:
        print e


def user_unicode_patch(self):
    return '%s' % (self.email)

User.__unicode__ = user_unicode_patch
User._meta.get_field('email')._unique = True


class OlarkChatGroup(models.Model):
    """ Olark Chart Group """

    operator_group = models.CharField(max_length=150, unique=True, blank=False)
    programs = models.ManyToManyField(Team, blank=True, null=True)
    target_location = models.ManyToManyField(Location, blank=True, null=True)
    google_rep = models.ManyToManyField(User, blank=True, null=True)
    olark_script = models.TextField(blank=False)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    def program_list(self):
        return ", ".join(["%s" % (p.team_name) for p in self.programs.all()])

    def location_list(self):
        return ", ".join(["%s" % (l.location_name) for l in self.target_location.all()])

    def rep_list(self):
        return ", ".join(["%s" % (r.get_full_name()) for r in self.google_rep.all()])

    class Meta:
        db_table = 'olark_chat_group'
        verbose_name_plural = 'Olark Chat Group'


class ResourceFAQ(models.Model):

    task_type = models.CharField(max_length=150, blank=False)
    task_question = models.TextField(blank=False)
    submited_by = models.ForeignKey(User)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __str__(self):
        return self.task_type

    class Meta:
        db_table = 'resource_faq'
        verbose_name_plural = 'ResourceFAQ'


class WPPMasterList(models.Model):

    customer_id = models.CharField(max_length=50, blank=True, null=True)
    provisional_assignee = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    server = models.CharField(max_length=100, blank=True, null=True)
    framework = models.CharField(max_length=100, blank=True, null=True)
    cms = models.CharField(max_length=100, blank=True, null=True)
    ecommerce = models.CharField(max_length=100, blank=True, null=True)
    priority = models.IntegerField(max_length=4, default=1)
    treatment_type = models.ForeignKey(TreatmentType, blank=True, default=None, null=True)
    notes = models.TextField(blank=True)

    YEAR_CHOICES = []
    for r in range(2000, (datetime.utcnow().year + 2)):
        YEAR_CHOICES.append((r, r))

    quarter = models.CharField(max_length=10, blank=False, choices=(
        ('Q1', 'Q1'),
        ('Q2', 'Q2'),
        ('Q3', 'Q3'),
        ('Q4', 'Q4'),)
    )
    year = models.IntegerField(max_length=4, choices=YEAR_CHOICES, default=datetime.utcnow().year)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        unique_together = ('customer_id', 'quarter', 'year')
        db_table = 'wpp_master_list'
        verbose_name_plural = "WPP Master List"
