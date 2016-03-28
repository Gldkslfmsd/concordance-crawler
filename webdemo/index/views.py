from django.shortcuts import render


# Create your views here.
from django.http import HttpResponse
from django.template import loader

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
	return render(request, 'index/browsejobs.html')
	
def jobdetail(request, job_id):
	context = { "id": job_id}
	return render(request, 'index/jobdetail.html', context)


