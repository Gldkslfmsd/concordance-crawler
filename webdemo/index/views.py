from django.shortcuts import render


# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import *

from .bratrsky import bratrsky

def index(request):
	context = {
		'jobs': [1, 2, 3, 4, 5]
	}
	return render(request, 'index/index.html', context)

def about(request):
	return render(request, 'index/about.html')

def createjob(request):
	return render(request, 'index/createjob.html')

def browsejobs(request, text=None):
	if text:
		context = { "jobs": bratrsky(text) }
	else:
		context = {}
	return render(request, 'index/browsejobs.html', context)
	
def jobdetail(request, job_id):
	context = { "id": job_id}
	return render(request, 'index/jobdetail.html', context)

def create(request, *args, **kwargs):
	try:
		request.POST['choice']
	except KeyError:
		return render(request, 'index/createjob.html', 
			{ 'error_message': "You didn't select a choice.", }
		)
	return browsejobs(request, request.POST['choice'])#render(request, 'index/about.html')
