from django.conf.urls.defaults import *

urlpatterns = patterns('monit.views',
    url(r'^collector$', 'collector', name='monit_collector'),
    url(r'^servers/$', 'server_list', name='server_list'),
    url(r'^servers/(?P<server_name>\w+)/$', 'server_detail', name='server_detail'),
    #url(r'^servers/(?P<monit_id>\w+)/services/$', 'service_list', name='service_list'),
    url(r'^servers/(?P<server_name>\w+)/services/(?P<service_name>[\w\-\.]+)/$', 'service_detail', name='service_detail'),
   
    )
