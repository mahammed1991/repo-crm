from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from main import views
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import Context

#import datetime
import json
from leads.models import Leads, WPPLeads, PicassoLeads
from datetime import datetime,timedelta
from collections import OrderedDict
from leads.models import Location, Timezone
import pytz 
from reports.models import Region

from django.http import Http404
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group

# Create your views here.
@login_required
def crm_management(request):
	if request.user.groups.filter(name='CRM-MANAGER'):
		# import ipdb; ipdb.set_trace()
		leads_list = list()
		limit = 10
		on_page = request.GET.get('page', 1)
		if on_page == 1:
			offset = 0
		else:
			offset = limit * on_page - 1 

		regions = Region.objects.all()
		if request.is_ajax():
			process_type = ''
			lead_status =  ''
			lead_sub_status = ''
			lead_appointment = None
			if request.GET.get('process'):
				process_type = request.GET.get('process')
			if request.GET.get('status'):
				lead_status = request.GET.get('status')
			if request.GET.get('sub_status'):
				lead_sub_status = request.GET.get('sub_status')
			if request.GET.get('appointment'):
				lead_appointment = request.GET.get('appointment')    


			if not lead_appointment:
				if lead_status == lead_sub_status:
					query = {'lead_status': lead_status}
				else:
					query = {'lead_status' : lead_status,'lead_sub_status' :lead_sub_status}
				if process_type == "WPP":
					# print settings.PROCESS_TYPE_MAPPING.get(process_type), lead_status, lead_sub_status

					leads = WPPLeads.objects.filter(type_1__in = settings.PROCESS_TYPE_MAPPING.get("WPP"), **query).values(
						'id', 'sf_lead_id', 'customer_id', 'company', 'first_name', 'created_date','appointment_date', 'phone', 'phone_optional', 'country'
						)[offset:limit]
					leads_count = WPPLeads.objects.filter(type_1__in = settings.PROCESS_TYPE_MAPPING.get("WPP"), **query).count()
					# print "WPP", leads_count

				elif process_type == "Picasso Audits":
					# print settings.PROCESS_TYPE_MAPPING.get(process_type), lead_status, lead_sub_status

					leads = PicassoLeads.objects.filter(type_1__in = settings.PROCESS_TYPE_MAPPING.get("Picasso Audits"), lead_status = lead_status).values(
						'id', 'sf_lead_id', 'customer_id', 'company', 'first_name', 'created_date', 'phone', 'country')[offset:limit]
					leads_count = PicassoLeads.objects.filter(type_1__in = settings.PROCESS_TYPE_MAPPING.get("Picasso Audits"), lead_status = lead_status).count()
					# print "Picasso Audits", leads_count

				elif process_type == "RLSA":
					# print settings.PROCESS_TYPE_MAPPING.get(process_type), lead_status, lead_sub_status

					leads = Leads.objects.filter(type_1__in = settings.PROCESS_TYPE_MAPPING.get("RLSA"), **query).values(
						'id', 'sf_lead_id', 'customer_id', 'company', 'first_name', 'created_date', 'appointment_date', 'phone', 'phone_optional', 'country'
						).order_by('-created_date')[offset:limit]
					leads_count = Leads.objects.filter(type_1__in = settings.PROCESS_TYPE_MAPPING.get("RLSA"), **query).count()
					# print "RLSA", leads_count

				elif process_type == "Shopping":
					# print settings.PROCESS_TYPE_MAPPING.get(process_type), lead_status, lead_sub_status

					leads = Leads.objects.filter(type_1__in = settings.PROCESS_TYPE_MAPPING.get("Shopping"), **query).values(
						'id', 'sf_lead_id', 'customer_id', 'company', 'first_name', 'created_date', 'appointment_date', 'phone', 'phone_optional', 'country'
						)[offset:limit]
					leads_count = Leads.objects.filter(type_1__in = settings.PROCESS_TYPE_MAPPING.get("Shopping"), **query).count()
					# print "Shopping", leads_count

				elif process_type == "Shopping Argos":
					# print settings.PROCESS_TYPE_MAPPING.get(process_type), lead_status, lead_sub_status

					leads = Leads.objects.filter(type_1__in = settings.PROCESS_TYPE_MAPPING.get("Shopping Argos"), **query).values(
						'id', 'sf_lead_id', 'customer_id', 'company', 'first_name', 'created_date', 'appointment_date', 'phone', 'phone_optional', 'country'
						)[offset:limit]
					leads_count = Leads.objects.filter(type_1__in = settings.PROCESS_TYPE_MAPPING.get("Shopping Argos"), **query).count()
					# print "Shopping Argos", leads_count

				else: # Tag
					exclude_types = settings.PROCESS_TYPE_MAPPING.get("RLSA") + settings.PROCESS_TYPE_MAPPING.get("Shopping Argos") + settings.PROCESS_TYPE_MAPPING.get("Shopping")
					# print exclude_types, lead_status, lead_sub_status
					leads = Leads.objects.exclude(type_1__in = exclude_types, **query).values('id', 'sf_lead_id', 'customer_id', 'company', 'first_name', 'created_date',  'appointment_date', 'phone', 'phone_optional', 'country'
						)[offset:limit]
					leads_count = Leads.objects.exclude(type_1__in = exclude_types, **query).count()
					# print "TAG",leads_count
					
			else:
				
				user_group = request.user.groups.filter(name='CRM-MANAGER')
				leads = get_filtered_leads(user_group,'TAG',lead_status,lead_sub_status,lead_appointment) 
				leads_count = leads.count()    
							 
			all_leads = get_leads(leads, leads_list)
			
			try:
				return HttpResponse(json.dumps({'leads_list': all_leads}), content_type="application/json")
			except Exception as e:
				print e

		context = {'crm_manager_text': json.dumps(settings.LEAD_STATUS_SUB_STATUS_MAPPING)}
		return render(request,'crm/manager_home.html',context)

	elif request.user.groups.filter(name='CRM-AGENT'):
		return redirect('mini_crm.views.crm_agent')
	else:
		raise Http404


def get_leads(leads, leads_list):
	for lead in leads:
		appointment_date = datetime.strftime(lead.get('appointment_date'), "%d/%m/%Y %I:%M %P") if lead.get('appointment_date') else lead.get('appointment_date') ,
		phone_optional =  lead.get('phone_optional')
		
		lead_dict = {
                     'id':lead['id'],
                     'sf_lead_id':lead['sf_lead_id'],
                     'c_id':lead['customer_id'],
					 'company':lead['company'], 
					 'customer_name':lead['first_name'],
					 'created_date':datetime.strftime(lead.get('created_date'), "%d/%m/%Y %I:%M %P") if lead.get('created_date') else lead.get('created_date'),  
					 'appointment_time': appointment_date,
					 'phone_number':lead['phone'], 
					 'additional_phone_number':phone_optional, 
					 'web_master_number':'', 
					 'location':lead['country']}
		
		leads_list.append(lead_dict)
	   
	return leads_list


def crm_agent(request):
	if request.user.groups.filter(name='CRM-MANAGER'):
		return redirect('mini_crm.views.crm_management')
	elif request.user.groups.filter(name='CRM-AGENT'):
		if request.is_ajax():
			leads_data = list()
			lead_status =  ''
			lead_sub_status = ''
			lead_appointment = None
			if request.GET.get('status'):
				lead_status = request.GET.get('status')
			if request.GET.get('sub_status'):
				lead_sub_status = request.GET.get('sub_status')
			if request.GET.get('appointment'):
				lead_appointment = request.GET.get('appointment')
			user_group = request.user.groups.filter(name='CRM-AGENT')
			leads = get_filtered_leads(user_group,'TAG',lead_status,lead_sub_status,lead_appointment)
			leads_data = get_json_leads(leads)
			response_json = leads_data
			res = HttpResponse(json.dumps(response_json), content_type="application/json")
			return res
		context ={
			'lead_status':settings.LEAD_STATUS_SUB_STATUS_MAPPING['TAG'].keys(),
			'lead_status_sub_status_mapping':json.dumps({'lead_status_sub_status_mapping':settings.LEAD_STATUS_SUB_STATUS_MAPPING},encoding="utf-8")
		}
		return render(request,'crm/agent_home.html',context)
	else:
		raise Http404


def get_filtered_leads(user_group,process,lead_status,lead_sub_status,lead_appointment):
	if lead_appointment and lead_appointment != 'Fresh Appointment':
		#Our Local timezone, to which we want to convert the UTC time.
		local_tz = pytz.timezone('Asia/Calcutta') 
		#Add Timezone information toUTC time.
		now_utc = pytz.utc.localize(datetime.now()) 
		# Convert to local time.
		local_time = now_utc.astimezone(local_tz) 
		local_time = local_time.replace(tzinfo=None)
		if lead_appointment == '30 minutes':
			start_date_time = local_time
			end_date_time = start_date_time + timedelta(minutes=30)
		if lead_appointment == '1 hour':
			start_date_time = local_time
			end_date_time = start_date_time + timedelta(minutes=60)
		if lead_appointment == 'Today':
			start_date_time = local_time.replace(hour=0,minute=0,second=0)
			end_date_time = local_time.replace(hour=23,minute=59,second=59)
		if lead_appointment == 'Tomorrow':
			tomorrow_date = local_time + timedelta(days=1)
			start_date_time = tomorrow_date.replace(hour=0,minute=0,second=0)
			end_date_time = tomorrow_date.replace(hour=23,minute=59,second=59)
		if lead_appointment == 'This week':
			current_date = local_time.date()
			year, week, dow = current_date.isocalendar()
			# Find the first day of the week.
			if dow == 7:
				# Since we want to start with Sunday, let's test for that condition.
				week_start = current_date
			else:
				# Otherwise, subtract `dow` number days to get the first day
				week_start = current_date - timedelta(dow)
			# Now, add 6 for the last day of the week (i.e., count up to Saturday)
			week_end = week_start + timedelta(6)
			start_date_time = datetime.combine(week_start, datetime.min.time()).replace(hour=0,minute=0,second=0)
			end_date_time =  datetime.combine(week_end, datetime.min.time()).replace(hour=23,minute=59,second=59)
		if user_group[0].name == 'CRM-AGENT':
			leads = Leads.objects.filter(lead_status="In Queue", appointment_date_in_ist__gte=start_date_time,appointment_date_in_ist__lte=end_date_time)
		else:
			#manager
			leads = Leads.objects.filter(lead_status="In Queue", appointment_date_in_ist__gte=start_date_time,appointment_date_in_ist__lte=end_date_time).values('customer_id', 'company', 'first_name', 'created_date',  'appointment_date', 'phone', 'phone_optional', 'country')
	else:
		if  user_group[0].name == 'CRM-AGENT':
			leads = Leads.objects.filter(lead_status=lead_status,lead_sub_status=lead_sub_status)
		else:
			#manager
			leads = Leads.objects.filter(lead_status=lead_status,lead_sub_status=lead_sub_status).values('customer_id', 'company', 'first_name', 'created_date',  'appointment_date', 'phone', 'phone_optional', 'country')

	return leads

def get_json_leads(leads):
	leads_data = list()
	for lead in leads:
		lead_dict = {
		'lead_owner':lead.lead_owner_name,
		'lead_status':lead.lead_status,
		'lead_sub_status':lead.lead_sub_status,
		'lead_id':lead.id,
		'customer_id':lead.customer_id,
		'company':lead.company,
		'customer_name':lead.first_name + '' + lead.last_name,
		'appointment_time':datetime.strftime(lead.appointment_date, "%d/%m/%Y %I:%M %P") if lead.appointment_date else '',
		'phone':lead.phone,
		'phone_optional':lead.phone_optional,
		'web_master_no':'',
		'location':'',
		'rescheduled':True if lead.rescheduled_appointment else False,
		'lead_owner_name':lead.lead_owner_name,
		'team':lead.team,
		'date_of_installation':datetime.strftime(lead.date_of_installation, "%d/%m/%Y") if lead.date_of_installation else '',
		'first_contacted_on':datetime.strftime(lead.first_contacted_on, "%d/%m/%Y %I:%M %P") if lead.first_contacted_on else '',
		'dials':lead.dials
		}
		if lead_dict['appointment_time']:
			date_time = lead_dict['appointment_time'].split(' ')
			lead_dict['apmnt_date'] = date_time[0]
			lead_dict['apmnt_time'] = date_time[1] + ' ' + date_time[2]	


@login_required
def lead_history(request):
    if request.user.groups.filter(name='CRM-AGENT'):
        lead_status = request.GET.get('status')
        if request.is_ajax():
            if lead_status == 'In Queue':
                leads = Leads.objects.filter(lead_status=lead_status)
            else:
                leads = Leads.objects.filter(appointment_date__isnull=False,rescheduled_appointment__isnull=False,lead_status='In Progress',lead_sub_status__in=['IP - CALL BACK','IP - Appointment Rescheduled - IS (GS)','IP - Code Sent'])
            leads_data = get_json_leads(leads)
            response_json = leads_data
            res = HttpResponse(json.dumps(response_json), content_type="application/json")
            return res
        return render(request,'crm/lead_and_history.html')
    else:
        raise Http404       


@login_required
def search_leads(request):
    searching_lead_id = request.GET.get('q')
    returning_data = list()
    try:
        normal_leads = Leads.objects.values('customer_id', 'type_1', 'url_1', 'lead_status').filter(Q(customer_id=searching_lead_id) | Q(sf_lead_id=searching_lead_id))
        if normal_leads:
            returning_data += list(normal_leads)
    except ObjectDoesNotExist:
        pass
    try:
        picasso_leads = PicassoLeads.objects.values('customer_id', 'type_1', 'url_1', 'lead_status').filter(Q(customer_id=searching_lead_id) | Q(sf_lead_id=searching_lead_id))
        if picasso_leads:
            returning_data += list(picasso_leads)
    except ObjectDoesNotExist:
        pass
    try:
        wpp_leads = WPPLeads.objects.values('customer_id', 'type_1', 'url_1', 'lead_status').filter(Q(customer_id=searching_lead_id) | Q(sf_lead_id=searching_lead_id))
        if wpp_leads:
            returning_data += list(wpp_leads)
    except ObjectDoesNotExist:
        pass

    return render(request,'crm/search_result.html',{'returning_data':returning_data, 'resultcount':len(returning_data),'q_id':searching_lead_id})


@login_required
def lead_details(request, lid, sf_lead_id):
    context = {}
    lead = None
    picassolead = None
    wpplead = None

    try:
        lead = Leads.objects.get(id=lid,sf_lead_id=sf_lead_id)
        wpplead = WPPLeads.objects.get(id=lid,sf_lead_id=sf_lead_id)
        picassolead = PicassoLeads.objects.get(id=lid,sf_lead_id=sf_lead_id)
        
    except ObjectDoesNotExist:
        print "no leads"
    
    if lead:
        context['lead'] = lead
    elif wpplead:
        context['lead'] = wpplead
    else:
        context['lead'] = picassolead

    return render(request,'crm/lead_details.html',context)

def lead_owner_avalibility(request):
    lead_owner = request.GET.get('lead_owner_email')
    lead_id = request.GET.get('id')
    lead_type = request.GET.get('type')
    
    user = User.objects.get(email=lead_owner)
    assignee_lead = Leads.objects.get(id=lead_id)   
    assignee_wpp_lead = Leads.objects.get(id=lead_id)   
    assignee_picasso_lead = Leads.objects.get(id=lead_id)

    try:
        leads = Leads.objects.filter(type_1=lead_type,lead_owner_email=lead_owner,lead_status__in=['Attempting Contact','In Queue','ON CALL','In Progress'])
        wppleads = WPPLeads.objects.filter(id=lead_id,type_1=lead_type)
        picassoleads = PicassoLeads.objects.filter(id=lead_id,type_1=lead_type)        
    except ObjectDoesNotExist:
        print "no leads"
    
    resp = {}

    if assignee_lead.appointment_date_in_ist is None or request.GET.get('override_appointment'):
        assignee_lead.lead_owner_name = user.first_name + ' ' + user.last_name
        assignee_lead.lead_owner_email = user.email
        assignee_lead.save()
        resp['success'] = True
    else:
        if leads:
            for i in leads:
                if assignee_lead.appointment_date_in_ist == i.appointment_date_in_ist:
                    resp['success'] = False
                else:
                    resp['success'] = True
                    assignee_lead.lead_owner_name = user.first_name + ' ' + user.last_name
                    assignee_lead.lead_owner_email = user.email
                    assignee_lead.save()
                    break;
        elif wppleads:
            for i in wppleads:
                if assignee_wpp_lead.appointment_date_in_ist == i.appointment_date_in_ist:
                    resp['success'] = False
                else:
                    resp['success'] = True
                    assignee_lead.lead_owner_name = user.first_name + ' ' + user.last_name
                    assignee_lead.lead_owner_email = user.email
                    assignee_lead.save()
                    break;
        elif picassoleads:
            for i in picassoleads:
                if assignee_picasso_lead.appointment_date_in_ist == i.appointment_date_in_ist:
                    resp['success'] = False
                else:
                    resp['success'] = True
                    assignee_lead.lead_owner_name = user.first_name + ' ' + user.last_name
                    assignee_lead.lead_owner_email = user.email
                    assignee_lead.save()
                    break;
        # else:
        #     resp['success'] = True
        #     assignee_lead.lead_owner_name = user.first_name + ' ' + user.last_name
        #     assignee_lead.lead_owner_email = user.email
        #     assignee_lead.save()

    return HttpResponse(json.dumps(resp))