from feeds import *
from utils.easyfeed import render_feed
from utils.common import get_full_path

def books(request):
    return render_feed(BooksFeed(get_full_path(request)))

def book(request, book_id):
    return render_feed(BookFeed(get_full_path(request), book_id))

def bookcomments(request, book_id):
    return render_feed(BookCommentsFeed(get_full_path(request), book_id))
