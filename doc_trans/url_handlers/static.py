# -*- coding: utf-8 -*-
from django.views.static import serve as static_serve
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.conf import settings

import os
index_names = ['index.html', 'index.htm', 'default.html', 'default.htm']

def serve(request, project_object, path):
    if len(path.split('/')) == 2 and path.split('/')[0] in (settings.ORIGINAL_LANGUAGE,settings.TRANSLATION_LANGUAGE) and path.split('/')[1] == '':
        for index_name in index_names:
            print os.path.join(settings.WEB_DOCS_DIR, project_object.slug, path.split('/')[0], index_name)
            if os.path.exists(os.path.join(settings.WEB_DOCS_DIR, project_object.slug, path.split('/')[0], index_name)):
                return HttpResponseRedirect(request.path + index_name)
    return static_serve(request, path, document_root=os.path.join(settings.WEB_DOCS_DIR, project_object.slug), show_indexes=False)