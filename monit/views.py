from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from monit.models import collect
import logging

#FIXME add auth & perms
@csrf_exempt
def collector(request):
    #TODO need to dig more into the monit collector protocol

    # only allow POSTs
    if not request.POST:
        return HttpResponseNotAllowed(['POST'])

    # make sure they gave us some data
    data = request.raw_post_data
    if data is None or len(data) == 0:
        return HttpResponseBadRequest('need some data')

    logging.info('monit collecter processing data from %s' % request.META['REMOTE_ADDR'])
    collect(data)
    return HttpResponse('ok')
