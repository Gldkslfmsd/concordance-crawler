from django.db import models

# Create your models here.

from os import listdir

JOBDIR = "jobs/"

def get_jobs():
	return listdir(JOBDIR)

def get_jobdetail(job_id):
	x = ""
	with open(JOBDIR+job_id+"/info","r") as f:
		x = f.read()
	return x
		
	
