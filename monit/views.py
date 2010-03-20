from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from monit.models import collect

#FIXME add auth & perms
def collector(request):
    #TODO need to dig more into the monit collector protocol
    
    # only allow POSTs
    if not request.POST:
        return HttpResponseNotAllowed(['POST'])

    # make sure they gave us some data
    data = request.raw_post_data
    if data is None or len(data) == 0:
        return HttpResponseBadRequest('need some data')

    collect(data)
    return HttpResponse('ok')
