from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='about'),
	url(r'^browsejobs/', views.browsejobs, name='browsejobs'),
	url(r'^jobdetail/(?P<job_id>[0-9]*)/?$', views.jobdetail, name='jobdetail'),
	url(r'^createjob/', views.createjob, name='createjob'),
		]
