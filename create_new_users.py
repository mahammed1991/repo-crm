# from google_portal import settings
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "google_portal.settings")
from django.conf import settings
from main.models import UserDetails
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

NEW_USERS = ["abhirami",
             "abiwalker",
             "aidenyoon",
             "aishwaryaranga",
             "alexiaa",
             "charujoshi",
             "choinmo",
             "csamuelson",
             "davidmanigand",
             "ecahalane",
             "eunahlee",
             "fsato",
             "galith",
             "guneetkhanuja",
             "guyrousso",
             "jaekyuna",
             "jakejac",
             "jananik",
             "madhavprasanna",
             "marctanguy",
             "marinaso",
             "minakim",
             "mooneyr",
             "murphys",
             "nmonahan",
             "oran",
             "philipcoyle",
             "racheltaylor",
             "raunaqrsherali",
             "ravalireddy",
             "rballett",
             "sagibracha",
             "sarstedt",
             "shauryabansal",
             "shlomitr",
             "spenumala",
             "teslo",
             "yamadateru",
             "yasminjilla",
             "yjcho",
             "ytlemcani"
             ]

domain = 'google.com'

new_user_count = 0

for username in NEW_USERS:
    email = "%s@%s" % (username, domain)
    try:
        new_user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        new_user = User()
        new_user.username = username
        new_user.email = email
        new_user.first_name = username
        new_user.save()
        new_user.groups.add(2)

        user_profile = UserDetails()
        user_profile.user_id = new_user.id
        user_profile.save()
        new_user_count += 1

print "No of new Users created: %s " % (new_user_count)
