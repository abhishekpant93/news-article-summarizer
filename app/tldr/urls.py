from django.conf.urls import patterns, url
from tldr import views

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
	url(r'^summary/$', views.summary, name='summary'), 
)