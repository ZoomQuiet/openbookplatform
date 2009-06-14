# Author: limodou@gmail.com
# version: 0.2
# Format the request and response from/to json and other format
#
# Update:
#  0.1 support json format
#  0.2 support xmlrpc, html format 
#

from django.http import HttpResponse
from utils.ajax import json_response
from django.conf import settings

class FormatMiddleware(object):
    def process_request(self, request):
        format_string = getattr(settings, 'FORMAT_STRING', 'format')
        format = request.GET.get(format_string, '')
        if format:
            request.format = format.lower() #could be "json", "xmlrpc", etc
        else:
            request.format = getattr(settings, 'DEFAULT_FORMAT', 'json')
        if request.format == 'xmlrpc':
            import xmlrpclib
            p, u = xmlrpclib.getparser()
            p.feed(request.raw_post_data)
            p.close()
            
            args = u.close()
            if len(args) > 0:
                args = args[0]
                if not isinstance(args, dict):
                    xml = xmlrpclib.dumps(xmlrpclib.Fault(-32400, 'system error: %s' % 'Arguments should be a dict'), methodresponse=1)				
                    return HttpResponse(xml, mimetype='text/xml; charset=utf-8')
                    
                old = request.POST._mutable
                request.POST._mutable = True
                for k, v in args.items():
                    request.POST[k] = v
                request.POST._mutable = old
            
    def process_response(self, request, response):
        if isinstance(response, HttpResponse):
            return response
        elif request.format == 'json':
            return json_response(response)
        elif request.format == 'xmlrpc':
            import xmlrpclib
            try:
            	xml = xmlrpclib.dumps((response,), methodresponse=1)
            except Exception, e:
            	xml = xmlrpclib.dumps(xmlrpclib.Fault(-32400, 'system error: %s' % e), methodresponse=1)				
            return HttpResponse(xml, mimetype='text/xml; charset=utf-8')
        elif request.format == 'html':
            if hasattr(request, 'format_processor'):
                return request.format_processor(response)
            else:
                return HttpResponse(response)
        raise Exception, 'Not support this format [%s]' % request.format
            
    
    