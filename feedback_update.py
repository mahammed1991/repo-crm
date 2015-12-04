import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "google_portal.settings")
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from main.models import Feedback
from leads.models import Leads


feedbacks = Feedback.objects.all()
failed_feedbacks = list()
for feedback in feedbacks:
    loc = feedback.location.location_name
    cid = feedback.cid
    lead_owner = feedback.lead_owner.email
    google_acc_manager = feedback.google_account_manager_id
    if google_acc_manager != 0:
        google_acc_manager = feedback.google_account_manager.email
    else:
        google_acc_manager = None
    query = {'customer_id': cid, 'country': loc, 'lead_owner_email': lead_owner}
    leads = Leads.objects.filter(**query)
    if leads and len(leads) > 1:
        query['google_rep_email'] = google_acc_manager
        leads = Leads.objects.filter(**query)
        if leads and len(leads) > 1:
            failed_feedbacks.append(feedback)
        else:
            leads = leads if leads else []
    else:
        failed_feedbacks.append(feedback)
    if len(leads) == 1:
        lead = leads[0]
        sf_lead_id = lead.sf_lead_id
        code_type = lead.type_1
        feedback.sf_lead_id = sf_lead_id
        feedback.code_type = code_type
        try:
            feedback.save()
        except ObjectDoesNotExist:
            print "error"
