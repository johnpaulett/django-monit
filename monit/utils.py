from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

def get_config(key, default=None):
    return getattr(settings, key, default)

def render_response(request, template, context):
    """Wrapper around render_to_response that adds the RequestContext."""
    return render_to_response(template, context,
                              context_instance=RequestContext(request))

