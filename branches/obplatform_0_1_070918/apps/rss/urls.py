from django.conf.urls.defaults import *
 
urlpatterns = patterns('',
    (r'^book/$', 'apps.rss.views.books'),
    (r'^book/(?P<book_id>\d+)/$', 'apps.rss.views.book'),
    (r'^book/(?P<book_id>\d+)/comments/$', 'apps.rss.views.bookcomments'),
)
