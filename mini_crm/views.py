from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
@login_required
def crm_management(request):
	if request.user.groups.filter(name='CRM-MANAGER'):
		print "yes"
		return redirect('mini_crm.views.manager_home')
	return render(request,'crm/agent_home.html',{})


def manager_home(request):
	if not request.user.groups.filter(name='CRM-MANAGER'):
		return redirect('mini_crm.views.crm_management')
	return render(request,'crm/manager_home.html',{})