from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from main import views


@login_required
def crm_management(request):
	if request.user.groups.filter(name='CRM-MANAGER'):
		return render(request,'crm/manager_home.html',{})
	elif request.user.groups.filter(name='CRM-AGENT'):
		return render(request,'crm/agent_home.html',{})
	else:
		return redirect('main.views.main_home')
