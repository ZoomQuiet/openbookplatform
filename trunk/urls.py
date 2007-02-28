from django.conf.urls.defaults import *
from django.conf import settings
from apps.users.decorator import check_valid_user
import apps.users.views.views
import apps.users.views.bookviews

urlpatterns = patterns('',
#    (r'^$', cache_page(apps.portal.views.index, 60*30)),
    (r'^$', 'apps.portal.views.index'),
    (r'^login/$', 'apps.portal.views.login'),
    (r'^logout/$', 'apps.users.views.auth.user_logout'),
    (r'^register/$', 'apps.users.views.auth.user_register'),
    (r'^license/$', 'apps.portal.views.license'),
    (r'^help/$', 'apps.portal.views.help'),
    
    (r'^user/(?P<object_id>\d+)/$', check_valid_user(apps.users.views.views.user_detail)),
    (r'^user/(?P<object_id>\d+)/edit/$', check_valid_user(apps.users.views.views.user_edit)),
    (r'^user/(?P<object_id>\d+)/saveportrait/$', check_valid_user(apps.users.views.views.user_save_portrait)),
    (r'^user/(?P<object_id>\d+)/book/ajax_list/$', check_valid_user(apps.users.views.bookviews.user_books_list)),
    (r'^user/(?P<object_id>\d+)/book/new/$', check_valid_user(apps.users.views.bookviews.user_book_edit)),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/$', check_valid_user(apps.users.views.bookviews.user_book_detail)),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/authors/$', check_valid_user(apps.users.views.bookviews.user_book_authors)),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/addauthor/$', check_valid_user(apps.users.views.bookviews.user_book_addauthor)),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/edit/$', check_valid_user(apps.users.views.bookviews.user_book_edit)),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/chapters/$', check_valid_user(apps.users.views.bookviews.user_book_chapters)),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/deletechapters/$', check_valid_user(apps.users.views.bookviews.user_chapters_delete)),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/chapter/(?P<chapter_id>\d+)/$', check_valid_user(apps.users.views.bookviews.user_chapter)),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/chapter/(?P<chapter_id>\d+)/comments/$', check_valid_user(apps.users.views.bookviews.user_chapter_comments)),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/chapter/(?P<chapter_id>\d+)/deletecomment/$', check_valid_user(apps.users.views.bookviews.user_chapter_delcomment)),
    (r'^user/(?P<object_id>\d+)/book/(?P<book_id>\d+)/addchapter/$', check_valid_user(apps.users.views.bookviews.user_chapter)),
    (r'^user/(?P<object_id>\d+)/book/delete/$', check_valid_user(apps.users.views.bookviews.user_books_delete)),
    (r'^user/(?P<object_id>\d+)/book/$', check_valid_user(apps.users.views.bookviews.user_books)),
    
    (r'^booklist/$', 'apps.books.views.booklist'),
    (r'^booklist/ajax_list/$', 'apps.books.views.ajax_list'),
    (r'^book/(?P<book_id>\d+)/$', 'apps.books.views.content'),
    (r'^book/(?P<book_id>\d+)/(?P<chapter_num>[^/]+)/commentsinfo/$', 'apps.books.views.chapter_comments_info'),
    (r'^book/(?P<book_id>\d+)/(?P<chapter_num>[^/]+)/addcomment/$', 'apps.books.views.add_comment'),
    (r'^book/(?P<book_id>\d+)/(?P<chapter_num>[^/]+)/allcomments/$', 'apps.books.views.chapter_comments'),
    (r'^book/(?P<book_id>\d+)/(?P<chapter_num>[^/]+)/(?P<comment_num>[^/]+)/$', 'apps.books.views.chapter_num_comments'),
    (r'^book/(?P<book_id>\d+)/(?P<chapter_num>[^/]+)/$', 'apps.books.views.chapter'),
    
    (r'^rss/', include('apps.rss.urls')),
    (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': settings.SITE_MEDIA}),
    (r'^admin/', include('django.contrib.admin.urls')),
)
