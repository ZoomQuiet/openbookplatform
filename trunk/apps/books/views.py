from apps.books.models import Book, Chapter
from utils.lib_page import Page
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from manipulator import AddCommentManipulator
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
    
def chapter_comments_info(request, book_id, chapter_num):
    chapter = Chapter.objects.get(num=chapter_num)
    objs = chapter.commentinfo_set.all()
    result = {}
    def _get_data(result, obj):
        result[obj.comment_num] = obj.count
    for obj in objs:
        _get_data(result, obj)
    
    return ajax.ajax_ok(result)
    
def add_comment(request, book_id, chapter_num):
    m = AddCommentManipulator(request, chapter_num)
    f, obj = m.validate_and_save(request)
    if f:
        return ajax.ajax_ok(message='ok')
    return ajax.ajax_fail(obj, message='error')
   
def _get_comment_data(result, obj):
    if obj.website:
        username = '<a rel="nofollow" href="%s">%s</a>' % (obj.website, obj.username)
    else:
        username = obj.username
    status = ''
    if obj.status == 1:
        status = '<span class="thanks" title="%s">√</span>' % obj.reply

    result.append({'username':username,
        'content':obj.content, 'status':status,
        'createtime':obj.createtime.strftime("%b %d,%Y %I:%m %p")})

def chapter_comments(request, book_id, chapter_num):
    chapter = Chapter.objects.get(num=chapter_num)
    objs = chapter.comment_set.all()
    result = []
    for obj in objs:
        _get_comment_data(result, obj)
    
    return ajax.ajax_ok(result)
    
def chapter_num_comments(request, book_id, chapter_num, comment_num):
    chapter = Chapter.objects.get(num=chapter_num)
    objs = chapter.comment_set.filter(comment_num=comment_num)
    result = []
    for obj in objs:
        _get_comment_data(result, obj)
    
    return ajax.ajax_ok(result)
