from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^$', 'apps.portal.views.index'),
    (r'^login/$', 'apps.portal.views.login'),
    (r'^logout/$', 'apps.users.views.auth.user_logout'),
    (r'^register/$', 'apps.users.views.auth.user_register'),
    (r'^license/$', 'apps.portal.views.license'),
    
    (r'^user/(?P<object_id>\d+)/$', 'apps.users.views.views.user_detail'),
    (r'^user/(?P<object_id>\d+)/edit/$', 'apps.users.views.views.user_edit'),
    (r'^user/(?P<object_id>\d+)/saveportrait/$', 'apps.users.views.views.user_save_portrait'),
    (r'^user/(?P<object_id>\d+)/book/ajax_list/$', 'apps.users.views.bookviews.user_books_list'),
    (r'^user/(?P<object_id>\d+)/book/new/$', 'apps.users.views.bookviews.user_book_edit'),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/$', 'apps.users.views.bookviews.user_book_detail'),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/edit/$', 'apps.users.views.bookviews.user_book_edit'),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/chapters/$', 'apps.users.views.bookviews.user_book_chapters'),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/deletechapters/$', 'apps.users.views.bookviews.user_chapters_delete'),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/chapter/(?P<chapter_id>\d+)/$', 'apps.users.views.bookviews.user_chapter'),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/addchapter/$', 'apps.users.views.bookviews.user_chapter'),
    (r'^user/(?P<object_id>\d+)/book/delete/$', 'apps.users.views.bookviews.user_books_delete'),
    (r'^user/(?P<object_id>\d+)/book/$', 'apps.users.views.bookviews.user_books'),
    
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
