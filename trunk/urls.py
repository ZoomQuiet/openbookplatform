from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^$', 'apps.portal.views.index'),
    (r'^license/$', 'apps.portal.views.license'),
    (r'^booklist/$', 'apps.books.views.list'),
    (r'^booklist/ajax_list/$', 'apps.books.views.ajax_list'),
    (r'^book/(?P<book_id>\d+)/$', 'apps.books.views.content'),
    (r'^book/(?P<book_id>\d+)/(?P<chapter_num>[^\s]+)/$', 'apps.books.views.chapter'),
    
    
    (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': settings.SITE_MEDIA}),
    (r'^admin/', include('django.contrib.admin.urls')),
)
