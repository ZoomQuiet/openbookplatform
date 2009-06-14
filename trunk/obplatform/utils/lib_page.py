from django.core.paginator import ObjectPaginator, InvalidPage
from django.db.models.query import QuerySet
import math

urlnames = {'next':_('Next'), 'previous':_('Previous'), 'first':_('First'), 'last':_('Last')}

class QuerysetWrapper(object):
    def __init__(self, t):
        self.list = t
        
    def count(self):
        return len(self.list)
    
    def __getslice__(self, i, j):
        return self.list[max(0, i):max(0, j):]

class Page(object):
    def __init__(self, queryset, request=None, pageno=1, paginate_by=15, urlprefix='', urlnames=urlnames):
        if isinstance(queryset, QuerySet):
            self.queryset = queryset
        else:
            self.queryset = QuerysetWrapper(queryset)
        self.paginate_by = paginate_by
        self.request = request
        self.urlprefix = urlprefix
        self.urlname = urlnames
        self.pageno = pageno
        
        paginator = ObjectPaginator(self.queryset, paginate_by)
        lastpage = math.ceil(1.0*self.queryset.count()/paginate_by)
        if self.request:
            page = self.request.GET.get('page', 1)
        else:
            page = self.pageno
        try:
            if isinstance(page, str):
                if not page.isdigit():
                    page = 'last'
                    page = lastpage
            page = int(page)
            if page > lastpage:
                page = lastpage
            object_list = paginator.get_page(page - 1)
        except (InvalidPage, ValueError):
            object_list = []
        self.is_paginated = paginator.pages > 1
        self.results_per_page = paginate_by
        self.has_next = paginator.has_next_page(page - 1)
        self.has_previous = paginator.has_previous_page(page - 1)
        self.page = page
        self.next = page + 1
        self.previous = page - 1
        self.pages = paginator.pages
        self.hits = paginator.hits
        self.object_list = object_list
        
    def next_url(self):
        if self.has_next:
            return '<a href="%spage=%d">%s</a>' % (self.fix_url(self.urlprefix), self.next, self.urlname['next'])
        else:
            return ''
        
    def previous_url(self):
        if self.has_previous:
            return '<a href="%spage=%d">%s</a>' % (self.fix_url(self.urlprefix), self.previous, self.urlname['previous'])
        else:
            return ''
        
    def first_url(self):
        if self.pages > 1:
            return '<a href="%spage=1">%s</a>' % (self.fix_url(self.urlprefix), self.urlname['first'])
        else:
            return ''
    
    def last_url(self):
        if self.pages > 1:
            return '<a href="%spage=%d">%s</a>' % (self.fix_url(self.urlprefix), self.pages, self.urlname['last'])
        else:
            return ''
        
    def fix_url(self, url):
        if url.find('?') == -1:
            url = url + '?'
        else:
            if not url.endswith('&') and not url.endswith('?'):
                url = url + '&'
        return url