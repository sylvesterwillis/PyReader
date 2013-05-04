from django.conf.urls import patterns, url

from rssfeedreader import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index')
)
