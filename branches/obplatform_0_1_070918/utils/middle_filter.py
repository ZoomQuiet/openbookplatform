# Author: limodou@gmail.com
# version: 0.1
# Url filter middleware
# Update:
#   0.1

from django.conf import settings
from utils.common import get_func
import re

class FilterMiddleware(object):
    def process_request(self, request):
        filter_items = getattr(settings, 'FILTERS', ())
        for v in filter_items:
            r, func = v
            if not isinstance(r, (list, tuple)):
                r = [r]
            for p in r:
                if isinstance(p, (str, unicode)):
                    p = re.compile(p)
                m = p.match(request.path[1:])
                if m:
                    kwargs = m.groupdict()
                    if kwargs:
                        args = ()
                    else:
                        args = m.groups()
                    return get_func(func)(request, *args, **kwargs)
            
