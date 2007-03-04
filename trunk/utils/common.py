def get_full_path(request):
    return 'http://' + request.META['HTTP_HOST'] + request.path

from django.template import RequestContext
from django.shortcuts import render_to_response
def render_template(request, template_path, extra_context = {}):
	c = RequestContext(request)
	c.update(extra_context)
	return render_to_response(template_path, context_instance=c)

def get_func(string):
    module, func = string.rsplit('.', 1)
    mod = __import__(module, {}, {}, [''])
    return getattr(mod, func)
    