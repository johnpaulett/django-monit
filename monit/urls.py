from django.conf.urls.defaults import *

urlpatterns = patterns('monit.views',
    url(r'^collector$', 'collector', name='monit_collector'),
    url(r'^servers/$', 'server_list', name='server_list'),
    url(r'^servers/(?P<server_name>\w+)/$', 'server_detail', name='server_detail'),
    url(r'^servers/(?P<server_name>\w+)/processes/(?P<process_name>[\w\-\.]+)/$', 'process_detail', name='process_detail'),
   
    )
