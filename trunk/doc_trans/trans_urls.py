# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from doc_trans.trans_views import *
import os
TRANS_MEDIA = os.path.abspath(os.path.join(os.path.dirname(__file__), 'media'))

urlpatterns = patterns('',
    url(r'^$', index, name="doc_trans-trans-index"),
    url(r'^project/([\w-]+)/$', project_page_list, name="doc_trans-trans-project-page-list"),
    url(r'^project/([\w-]+)/versions/$', project_versions, name="doc_trans-trans-project-versions"),
    url(r'^project/([\w-]+)/comments/$', project_comments, name="doc_trans-trans-project-comments"),
    url(r'^project/([\w-]+)/versions/#revision-([\w]+)$', project_version, name="doc_trans-trans-project-version"),
    url(r'^project/([\w-]+)/(join|quit)/$', project_join_quit, name="doc_trans-trans-project-join-quit"),
    url(r'^project/([\w-]+)/(.+)$', project_page_list, name="doc_trans-trans-project-dir-page-list"),
    
    url(r'^page/([\w-]+)/([\w-]+)/$', page_trans, name="doc_trans-trans-page-trans"),
    url(r'^page/([\w-]+)/([\w-]+)/changes/$', page_changes, name="doc_trans-trans-page-changes"),
    url(r'^page/([\w-]+)/([\w-]+)/comments/$', page_comments, name="doc_trans-trans-page-comments"),
    url(r'^page-changes/([\w-]+)/([\w-]+)/([\w-]+)/$', page_version_changes, name="doc_trans-trans-page-version-changes"),
    
    url(r'^paragraph/(\d+)/translation/$', paragraph_translation, name="doc_trans-trans-paragraph-translation"),
    url(r'^paragraph/(\d+)/histories/$', paragraph_histories, name="doc_trans-trans-paragraph-histories"),
    url(r'^paragraph/(\d+)/comments/$', paragraph_comments, name="doc_trans-trans-paragraph-comments"),
    url(r'^paragraph/(\d+)/translation/histories/$', paragraph_translation_histories, name="doc_trans-trans-paragraph-translation-histories"),
    
    url(r'^people/$', people_list, name="doc_trans-trans-people-list"),
    url(r'^people/([\w-]+)/$', people, name="doc_trans-trans-people"),
    
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': TRANS_MEDIA, 'show_indexes': True}, name = 'doc_trans-trans-media'),
    
    url(r'^help/$', help, name="doc_trans-trans-help"),
    
    url(r'^i18n/setlang/$', setlang, name="doc_trans-trans-setlang"),

)
