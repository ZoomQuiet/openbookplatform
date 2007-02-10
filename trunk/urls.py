from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^$', 'apps.portal.views.index'),
    (r'^login/$', 'apps.users.views.auth.user_login'),
    (r'^logout/$', 'apps.users.views.auth.user_logout'),
    (r'^register/$', 'apps.users.views.auth.user_register'),
    (r'^license/$', 'apps.portal.views.license'),
    (r'^booklist/$', 'apps.books.views.list'),
    (r'^booklist/ajax_list/$', 'apps.books.views.ajax_list'),
    (r'^book/(?P<book_id>\d+)/$', 'apps.books.views.content'),
    (r'^book/(?P<book_id>\d+)/(?P<chapter_num>[^/]+)/commentsinfo/$', 'apps.books.views.chapter_comments_info'),
    (r'^book/(?P<book_id>\d+)/(?P<chapter_num>[^/]+)/addcomment/$', 'apps.books.views.add_comment'),
    (r'^book/(?P<book_id>\d+)/(?P<chapter_num>[^/]+)/allcomments/$', 'apps.books.views.chapter_comments'),
    (r'^book/(?P<book_id>\d+)/(?P<chapter_num>[^/]+)/(?P<comment_num>[^/]+)/$', 'apps.books.views.chapter_num_comments'),
    (r'^book/(?P<book_id>\d+)/(?P<chapter_num>[^/]+)/$', 'apps.books.views.chapter'),
    
    (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': settings.SITE_MEDIA}),
    (r'^admin/', include('django.contrib.admin.urls')),
)
