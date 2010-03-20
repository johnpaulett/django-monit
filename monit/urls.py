from django.conf.urls.defaults import *

urlpatterns = patterns('monit.views',
    url(r'^collector$', 'collector', name='monit_collector'),
)
