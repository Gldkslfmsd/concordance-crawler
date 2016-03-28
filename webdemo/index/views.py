from django.shortcuts import render


# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import *

def index(request):
	context = {
		'jobs': [1, 2, 3, 4, 5]
	}
	return render(request, 'index/index.html', context)

def about(request):
	return render(request, 'index/about.html')

def createjob(request):
	return render(request, 'index/createjob.html')

def browsejobs(request):
	context = { "jobs": get_jobs()+[get_jobdetail("1")] }
	return render(request, 'index/browsejobs.html', context)
	
def jobdetail(request, job_id):
	context = { "id": job_id}
	return render(request, 'index/jobdetail.html', context)

def create(request, *args, **kwargs):
	print(request.POST)
	try:
		request.POST['choice']
	except KeyError:
		print("keyerror!!!")
		return render(request, 'index/createjob.html', 
			{ 'question': 1, 'error_message': "You didn't select a choice.", }
		)
	print(args)
	print(request.POST)
	return browsejobs(request)#render(request, 'index/about.html')
