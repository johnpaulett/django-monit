from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_exempt
from monit.models import collect, Server, Service
from monit.utils import get_config, render_response

import logging

@csrf_exempt
@user_passes_test(lambda user: get_config('MONIT_AUTHENTICATE', False) && user.has_perm('server.can_post_data'))
def collector(request):
    #TODO need to dig more into the monit collector protocol

    # only allow POSTs
    if not request.POST:
        return HttpResponseNotAllowed(['POST'])

    # make sure they gave us some data
    data = request.raw_post_data
    if data is None or len(data) == 0:
        return HttpResponseBadRequest('need some data')

    logging.info('monit collecter processing data from %s' %
                 request.META['REMOTE_ADDR'])
    collect(data)
    return HttpResponse('ok')

def server_list(request, template_name='monit/server_list.html'):
    servers = get_list_or_404(Server)
    return render_response(request, template_name,
                           {'servers': servers})

def server_detail(request, server_name,
                  template_name='monit/server_detail.html'):
    server = get_object_or_404(Server, localhostname=server_name)
    processes = server.process_set.all()
    return render_response(request, template_name,
                           {'server': server, 'processes': processes})

def process_detail(request, server_name, process_name,
                   template_name='monit/process_detail.html'):
    server = get_object_or_404(Server, localhostname=server_name)
    process = get_object_or_404(server.process_set.all(), name=process_name)
    return render_response(request, template_name,
                           {'server': server, 'process': process})
    
