# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from doc_trans.views import *

document_root = os.path.abspath(os.path.join(os.path.dirname(__file__), 'docs', '_build', 'html'))

urlpatterns = patterns('',
    url(r'^$', project_list, name="doc_trans-docs-project-list"),
    url(r'^#([\w-]+)$', project_index, name="doc_trans-docs-project-index"),
    (r'^self-docs/(?P<path>.*)$', 'django.views.static.serve', {'document_root': document_root, 'show_indexes': True}),
    url(r'^([\w-]+)/(.*)$', project_serve, name="doc_trans-docs-project-serve"),
)
