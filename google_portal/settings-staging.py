"""
Django settings for google_portal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm_=j)c^5#3p+jo4yiupue)z39a90dd@y*rflz=+g5b7i=@ns#j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['10.250.2.21', '202.140.38.95', 'gtrack.regalixdev.com', 'wpp.regalixdev.com', 'picasso.regalixdev.com']

ROOT_URLCONF = 'google_portal.urls'

WSGI_APPLICATION = 'google_portal.wsgi-staging.application'

CACHE_MAX_KEY_LENGTH = 235

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gtrack',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = False


STATIC_FOLDER = os.path.join(BASE_DIR, "static")

# TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'))
TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'forum/skins/default/templates'),
]

# Application constants
PORTAL_MAIL_ID = 'google@regalix-inc.com'
REGALIX_DEFAULT_ROLE = 1
GOOGLE_DEFAULT_ROLE = 3
ADMIN_DOMAIN = 'regalix-inc.com'
REGULAR_DOMAIN = 'gmail.com'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'google@regalix-inc.com'
EMAIL_HOST_PASSWORD = 'regalix123'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

DEFAULT_LEAD_OWNER_EMAIL = 'skamat@regalix-inc.com'
DEFAULT_LEAD_OWNER_ROLE = 'RR'
DEFAULT_LEAD_OWNER_FNAME = 'Suri'
DEFAULT_LEAD_OWNER_LNAME = 'Kamat'

BCC_EMAIL = 'gtracktesting@gmail.com'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Media Files (User uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = "/srv/gtrack-uploads"

# URLs for login, post login redirect and error
LOGIN_URL = '/auth/login'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/auth/post_login/'
LOGIN_ERROR_URL = '/auth/error'

TAG_URL = 'http://gtrack.regalixdev.com'
WPP_URL = 'http://wpp.regalixdev.com'

# Social auth settings
# APP settings
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '124672404110-8i8oatin6gg2r2b8611o0qgmvmiuvlme.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'm9U_OqVgSYcLTQ8DFdjndo7B'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '306443257786-qav8khr2je2ocpftb4pg3pgjhc7h89e1.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'moS9p0suOUzkzAEWJGAsCWg9'

# Social Auth error handling
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = LOGIN_URL
SOCIAL_AUTH_BACKEND_ERROR_URL = LOGIN_URL

# Use email as username for user acccounts
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_GOOGLE_OAUTH2_USE_DEPRECATED_API = True

SOCIAL_AUTH_SESSION_EXPIRATION = False
SESSION_COOKIE_DOMAIN = ".regalixdev.com"

# list of domains allowed
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['regalix-inc.com', 'gmail.com']
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = []

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',

    'forum.context.application_settings',
    'django.contrib.messages.context_processors.messages',
    'forum.user_messages.context_processors.user_messages',
]

APPEND_SLASH = True

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'forum',
    'main',
    'auth',
    'leads',
    'newsletter',
    'representatives',
    'south',
    'reports',
    'kronos',
    'umm',
)

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
    'lib.middleware.StandardExceptionMiddleware',
    'lib.middleware.SetProfilePicture',

    # Forum related middleware classes
    'forum.middleware.request_utils.RequestUtils',
]

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'auth.views.check_email',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Use for generating reports
# lead status should be this order
LEAD_STATUS = ['In Queue', 'Attempting Contact', 'In Progress', 'In Active',
               'Implemented', 'ON CALL', 'Pending QC - WIN', 'Pending QC - In Active', 'Rework Required']

WPP_LEAD_STATUS = ['Open', 'On Hold', 'In UI/UX Review', 'In Mockup', 'Mockup Review',
                   'In Development', 'In Stage', 'In Stage - Adv Implementation', 'In A/B Test', 'Implemented', 'Deferred']

LEAD_STATUS_DICT = {'Attempting Contact': ['Attempting Contact'],
                    'In Progress': ['In Progress'],
                    'Implemented': ['Implemented', 'Pending QC - WIN'],
                    'In Active': ['In Active', 'Pending QC - In Active'],
                    'In Queue': ['In Queue', 'ON CALL'],
                    }

PICASSO_LEAD_STATUS = ['In Queue', 'Audited', 'Delivered']


SERVICES = ['Services', 'Services (Traverwood)', 'Services Revenue Program (SRP)']

CODE_TYPE_DICT = {'Adwords Conversion Code': ['Adwords Conversion Code', 'AdWords Conversion Tracking', 'Conversion Code'],
                  'Adwords Remarketing Code': ['Adwords Remarketing', 'Remarketing'], 'Analytics': ['Analytics'],
                  'Cross Domain Tracking': ['Analytics Cross Domain Tracking', 'Cross Domain Tracking'],
                  'Analytics Destination Tracking': ['Analytics Destination Tracking', 'GA Destination Tracking'],
                  'Analytics E-Commerce Tracking': ['Analytics E-Commerce Tracking', 'GA E-Commerce Tracking'],
                  'Analytics Event Tracking': ['Analytics Event Tracking', 'GA Event Tracking'],
                  'Dynamic Remarketing - Retail': ['Dynamic Remarketing - Retail', 'Dynamic Remarketing'],
                  'Dynamic Remarketing - Extension (non retail)': ['Dynamic Remarketing - Extension (non retail)'],
                  'Google Analytics Remarketing': ['GA Remarketing', 'Google Analytics Remarketing Tracking'],
                  'Website Call Conversion': ['Website Call Conversion', 'Google Forwarding Numbers Conversion code'],
                  'Google Shopping Setup': ['Google Shopping Setup'], 'Google Tag Manager': ['Google Tag Manager'],
                  'SDK Conversion Tracking': ['Mobile Conversion Tracking', 'SDK Conversion Tracking'],
                  'Google Shopping Migration': ['Google Shopping Migration'], 'GA Conversion Tracking': ['GA Conversion Tracking'],
                  'Google Analytics Dynamic Remarketing  (Retail)': ['Google Analytics Dynamic Remarketing  (Retail)'],
                  'WCC Beta': ['WCC Beta'],
                  'Analytics Enhanced E-Commerce Tracking': ['Analytics Enhanced E-Commerce Tracking']}

FILE_UPLOAD_TEMP_DIR = os.path.join(os.path.dirname(__file__), 'tmp').replace('\\', '/')
FILE_UPLOAD_HANDLERS = ("django.core.files.uploadhandler.MemoryFileUploadHandler",
                        "django.core.files.uploadhandler.TemporaryFileUploadHandler",
                        )
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

ALLOW_FILE_TYPES = ('.jpg', '.jpeg', '.gif', '.bmp', '.png', '.tiff')
ALLOW_MAX_FILE_SIZE = 1024 * 1024

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


template_loaders = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'forum.modules.template_loader.module_templates_loader',
    'forum.skins.load_template_source',
)

SITE_SRC_ROOT = BASE_DIR

TEMPLATE_LOADERS = list(template_loaders) if DEBUG else [('django.template.loaders.cached.Loader', template_loaders)]

APP_URL = 'http://gtrack.regalixdev.com'


try:
    if len(FORUM_SCRIPT_ALIAS) > 0:
        APP_URL = '%s/%s' % (APP_URL, FORUM_SCRIPT_ALIAS[:-1])
except NameError:
    pass

app_url_split = APP_URL.split("://")

APP_PROTOCOL = app_url_split[0]
APP_DOMAIN = app_url_split[1].split('/')[0]
APP_BASE_URL = '%s://%s' % (APP_PROTOCOL, APP_DOMAIN)

FORCE_SCRIPT_NAME = ''

for path in app_url_split[1].split('/')[1:]:
    FORCE_SCRIPT_NAME = FORCE_SCRIPT_NAME + '/' + path

if FORCE_SCRIPT_NAME.endswith('/'):
    FORCE_SCRIPT_NAME = FORCE_SCRIPT_NAME[:-1]

# Module system initialization
MODULES_PACKAGE = 'forum_modules'
MODULES_FOLDER = os.path.join(SITE_SRC_ROOT, MODULES_PACKAGE)

OSQA_DEFAULT_SKIN = 'default'

DISABLED_MODULES = ['books', 'recaptcha', 'project_badges']

MODULE_LIST = filter(lambda m: getattr(m, 'CAN_USE', True), [
    __import__('forum_modules.%s' % f, globals(), locals(), ['forum_modules'])
    for f in os.listdir(MODULES_FOLDER) if os.path.isdir(os.path.join(MODULES_FOLDER, f)) and os.path.exists(os.path.join(MODULES_FOLDER, "%s/__init__.py" % f)) and not f in DISABLED_MODULES
])

[MIDDLEWARE_CLASSES.extend(
    ["%s.%s" % (m.__name__, mc) for mc in getattr(m, 'MIDDLEWARE_CLASSES', [])]) for m in MODULE_LIST]

[TEMPLATE_LOADERS.extend(["%s.%s" % (m.__name__, tl) for tl in getattr(m, 'TEMPLATE_LOADERS', [])]) for m in MODULE_LIST]

SFDC = 'STAGE'
TECH_TEAM_ID = '005d00000049PanAAE'

API_KEY = 'AIzaSyAV3QgE5ezDAVyXIFKO_QfYb1L-jT_cj30'

SFDC_FIELDS = "Id, LastName, FirstName, Name, Company, Phone, Email, Description, Status, CreatedDate,\
    gm_email__c, Customer_ID__c, First_Name_optional__c, Last_Name_optional__c, Phone_optional__c, Email_optional__c,\
    Code__c, URL__c, Code_Type__c, Regalix_Comment__c, Google_Comment__c, Code_2__c, Code_3__c, Code_4__c, Code_5__c,\
    URL_2__c, URL_3__c, URL_4__c, URL_5__c, Comment_2__c, Comment_3__c, Comment_4__c, Comment_5__c, Type_2__c, Type_3__c,\
    Type_4__c, Type_5__c, Appointment_Date__c, qbdialer__Dials__c, Comment_1__c, E_commerce__c, Location__c, X1st_Contact_on__c,\
    Primary_Contact_Email__c, Google_Rep__c, Date_of_installation__c, Team__c, Type_Of_Installation__c, Lead_Implemented_Date_Time__c,\
    Rescheduled_Appointments__c, Time_Zone__c, Lead_Sub_Status__c, Q2_Manager__c, WPP_Lead_Status__c, OwnerId, Reschedule_IST_Time__c,\
    Reschedule_IST__c, Treatment_Type__c, Additional_Notes_if_any__c, Mockup_URL__c, Mockup_URL_Password__c, Stage_URL__c,\
    Stage_URL_Credentials__c, AB_Testing__c, GCSS_Status__c, Language__c,  All_Regalix_Comments__c, Picasso_Objective__c,\
    Internal_CID_1__c, POD_Name__c, Picasso_Lead_Stage__c, PICASSO_build_eligible__c, Eligible_Nominated_for_WPP__c, Picasso_Reference_Id__c"

SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/16crEI36EeBDGuOx0GBusJ8gloH6zWsJNErf5opeavzE/edit#gid=782277640'
