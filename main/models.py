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


from leads.models import Location, Team


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
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='NEW')
    lead_owner = models.ForeignKey(User, related_name='lead_owner', default=default_lead_owner)
    program = models.ForeignKey(Team, default=None, null=True)

    attachment = models.FileField(upload_to=get_file_path)

    resolved_by = models.ForeignKey(User, related_name='resolved_by', null=True)
    resolved_date = models.DateTimeField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        return os.path.basename(self.attachment.name)

    class Meta:
        db_table = 'feedback'


class FeedbackComment(models.Model):
    """ Feedback comments """
    feedback = models.ForeignKey(Feedback)
    comment = models.CharField(max_length=1500)
    comment_by = models.ForeignKey(User)
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
    profile_photo_url = models.CharField(max_length=255, default=None, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)


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
        ('TL', 'TEAM LEADER'),
        ('MGMT', 'MANAGEMENT'),
        ('QA', 'QUALLITY ASSURANCE'),
        ('TECH', 'TECH'),
        ('TAG', 'TAG'),
        ('SHOPPING', 'SHOPPING'),
        ('PLA', 'PLA'),
        ('MIS', 'MIS'),
        ('DESIGN', 'DESIGN'),)
    )
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True)
    google_id = models.EmailField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    skype_id = models.CharField(max_length=100, blank=True, null=True)
    region = models.ForeignKey(Location, null=True, blank=True, default=None)
    profile_photo = models.ImageField(upload_to=get_profile_photo, blank=True, max_length=100)

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
            img = Image.open(image)
            w, h = img.size

            #validate dimensions
            max_width = 500
            max_height = 550
            if w > max_width or h > max_height:
                raise ValidationError(
                    _('Please use an image that is smaller or equal to '
                      '%s x %s pixels.' % (max_width, max_height)))

            #validate content type
            img_ext = image.name.split('.')[1]
            if not img_ext in ['png']:
                raise ValidationError(_('Image is not in PNG format. Please use a PNG image.'))

        return image

    class Meta:
        db_table = 'contact_list'
        ordering = ['first_name']


class CustomerTestimonials(models.Model):
    """ Customer Testimonials information """

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    statement_text = models.TextField(blank=False)
    email = models.EmailField(max_length=100, blank=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(default=datetime.utcnow())
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customer_testimonials'
        ordering = ['-created_date']
