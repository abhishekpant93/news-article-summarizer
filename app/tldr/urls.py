from django.conf.urls import patterns, url
from tldr import views

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
	url(r'^summarize/$', views.summarize, name='summarize'),
	url(r'^summary/$', views.summary, name='summary'),
	url(r'^summary_api/$', views.summary_api, name='summary_api'),
	url(r'^api_result/$', views.api_result, name='api_result') 
)