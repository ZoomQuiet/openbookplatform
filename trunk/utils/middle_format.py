# Author: limodou@gmail.com
# version: 0.1
# Format the request and response from/to json and other format
#

from django.http import HttpResponse
from utils.ajax import json_response
from django.conf import settings

class FormatMiddleware(object):
    def process_request(self, request):
        format_string = getattr(settings, 'FORMAT_STRING', 'format')
        format = request.GET.get(format_string, '')
        if format.lower() == 'json':
            request.format = 'json'
        else:
            request.format = getattr(settings, 'DEFAULT_FORMAT', 'json')

    def process_response(self, request, response):
        if isinstance(response, HttpResponse):
            return response
        elif request.format == 'json':
            return json_response(response)
            
    
    