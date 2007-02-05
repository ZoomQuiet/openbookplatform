from apps.books.models import Book, Chapter
from utils.lib_page import Page
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from utils import ajax

def list(request):
    user = request.user
    return render_to_response('books/list.html', 
        context_instance=RequestContext(request))


def _get_data(request, obj):
    if obj.icon:
        icon = '<img src="/site_media/%s" alt="%s"/>' % (obj.get_icon_url(), obj.title)
    else:
        icon = '<img src="/site_media/img/book_icon.jpg" alt="%s"/>' % obj.title
    authors = [x.username for x in obj.author.all()]
    return ({'id':obj.id, 'icon':icon, 'title':obj.title, 
        'description':obj.description, 'author':','.join(authors)})

def ajax_list(request):
    pagenum = 10
    result = []
    objs = Book.objects.all()
    page = Page(objs, request, paginate_by=pagenum)
    for o in page.object_list:
        result.append(_get_data(request, o))
    pages = (objs.count() + pagenum - 1) / pagenum
    cur = int(request.GET.get('page', 1))
    return ajax.ajax_ok((cur, pages, result))

def content(request, book_id):
    book = Book.objects.get(pk=int(book_id))
    return render_to_response('books/content.html', 
        context_instance=RequestContext(request, {'book':book}))
    
def chapter(request, book_id, chapter_num):
    book = Book.objects.get(pk=int(book_id))
    chapter = Chapter.objects.get(num=chapter_num)
    prev, next = None, None
    nexts = Chapter.objects.filter(num__gt=chapter_num)
    if nexts:
        next = nexts[0]
    prevs = Chapter.objects.filter(num__lt=chapter_num)
    if prevs:
        prev = prevs[0]
    return render_to_response('books/chapter.html', 
        context_instance=RequestContext(request, {'book':book, 
            'chapter':chapter, 'next':next, 'prev':prev}))
    