from utils.easyfeed import EasyFeed
from django.utils.translation import gettext_lazy as _
from apps.books.models import Book

class BooksFeed(EasyFeed):
    def __init__(self, feed_url):
        super(BooksFeed, self).__init__(feed_url)

    def link(self):
        return '/booklist/'
    
    def items(self):
        return Book.objects.all()[:15]
    
    def title(self):
        return u'Open Book Platform'
        
    def description(self):
        return u'Open Book Platform'
    
    def item_link(self, item):
        return '/book/%d/' % item.id
    
    def item_description(self, item):
        return item.description
        
    def item_title(self, item):
        return item.title
    
    def item_pubdate(self, item):
        return item.modifydate
       
    def item_author_name(self, item):
        return ','.join([x.username for x in item.authors.all()])
        
class BookFeed(EasyFeed):
    def __init__(self, feed_url, book_id):
        super(BookFeed, self).__init__(feed_url)
        self.book_id = book_id
        self.book = Book.objects.get(id=int(book_id))

    def link(self):
        return '/book/%s' % self.book_id
    
    def items(self):
        return self.book.chapter_set.all()[:15]
    
    def title(self):
        return self.book.title
        
    def description(self):
        return self.book.description
    
    def item_link(self, item):
        return '/book/%d/%s/' % (item.book.id, item.num)
    
    def item_description(self, item):
        return item.html
        
    def item_title(self, item):
        return item.title
    
    def item_pubdate(self, item):
        return item.modifydate
       
    def item_author_name(self, item):
        return ','.join([x.username for x in item.book.authors.all()])
    
class BookCommentsFeed(EasyFeed):
    def __init__(self, feed_url, book_id):
        super(BookCommentsFeed, self).__init__(feed_url)
        self.book_id = book_id
        self.book = Book.objects.get(id=int(book_id))

    def link(self):
        return '/book/%s' % self.book_id
    
    def items(self):
        return self.book.comment_set.all().order_by('-createtime')[:15]
    
    def title(self):
        return 'Comments of: ' + self.book.title
        
    def description(self):
        return self.book.description
    
    def item_link(self, item):
        return ''
    
    def item_description(self, item):
        return item.content
        
    def item_title(self, item):
        return '#%d Comment for: ' % item.id + item.chapter.title
    
    def item_pubdate(self, item):
        return item.createtime
       
    def item_author_name(self, item):
        return item.username
    
