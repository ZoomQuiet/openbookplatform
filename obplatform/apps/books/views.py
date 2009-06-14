#coding=utf-8
from apps.books.models import Book, Chapter
from utils.lib_page import Page
from apps.books.validator import AddCommentValidator
from utils import ajax
from utils.common import render_template

def booklist(request):
    user = request.user
    return render_template(request, 'books/list.html')


def _get_data(request, obj):
    if obj.icon:
        icon = '<img class="border" src="/site_media/%s" alt="%s"/>' % (obj.get_icon_url(), obj.title)
    else:
        icon = '<img class="border" src="/site_media/img/book_icon.jpg" alt="%s"/>' % obj.title
    authors = [x.username for x in obj.authors.all()]
    return ({'id':obj.id, 'icon':icon, 'title':obj.title, 
        'description':obj.description, 'author':','.join(authors),
        'modifydate':obj.modifydate.strftime("%b %d,%Y %I:%m %p")})

def ajax_list(request):
    pagenum = 10
    result = []
    objs = Book.objects.all()
    page = Page(objs, request, paginate_by=pagenum)
    for o in page.object_list:
        result.append(_get_data(request, o))
    pages = (objs.count() + pagenum - 1) / pagenum
    cur = int(request.GET.get('page', 1))
    return ajax.ajax_ok_data((cur, pages, result))

def content(request, book_id):
    book = Book.objects.get(pk=int(book_id))
    return render_template(request, 'books/content.html', {'book':book})
    
def chapter(request, book_id, chapter_num):
    book = Book.objects.get(pk=int(book_id))
    chapter = Chapter.objects.get(num=chapter_num, book=book)
    prev, next = None, None
    nexts = Chapter.objects.filter(num__gt=chapter_num, book=book)
    if nexts:
        next = nexts[0]
    prevs = Chapter.objects.filter(num__lt=chapter_num, book=book)
    if prevs:
        prev = list(prevs)[-1]
    return render_template(request, 'books/chapter.html', {'book':book, 
            'chapter':chapter, 'next':next, 'prev':prev, 'COOKIES':request.COOKIES})
    
def chapter_comments_info(request, book_id, chapter_num):
    book = Book.objects.get(pk=int(book_id))
    chapter = Chapter.objects.get(num=chapter_num, book=book)
    objs = chapter.commentinfo_set.all()
    result = {}
    def _get_data(result, obj):
        result[obj.comment_num] = obj.count
    for obj in objs:
        _get_data(result, obj)
    
    return ajax.ajax_ok(result)
    
from utils.easy_cookie import set_cookie

def add_comment(request, book_id, chapter_num):
    m = AddCommentValidator(request, book_id, chapter_num)
    f, obj = m.validate_and_save(request)
    if f:
        response = ajax.ajax_ok(message='ok')
        set_cookie(response, 'username', request.REQUEST.get('username', ''))
        set_cookie(response, 'email', request.REQUEST.get('email', ''))
        set_cookie(response, 'website', request.REQUEST.get('website', ''))
        return response
    return ajax.ajax_fail(obj, message='error')

from utils.textconvert import plaintext2html
def _get_comment_data(result, obj):
    if obj.website:
        username = '<a rel="nofollow" href="%s">%s</a>' % (obj.website, obj.username)
    else:
        username = obj.username
    status = ''
    if obj.status == 1:
        status = '<span class="thanks" title="%s">√</span>' % obj.reply
    if obj.html:
        content = obj.html
    else:
        content = plaintext2html(obj.content)

    result.append({'username':username,
        'content':content, 'status':status,
        'createtime':obj.createtime.strftime("%b %d,%Y %I:%m %p")})

def chapter_comments(request, book_id, chapter_num):
    book = Book.objects.get(pk=int(book_id))
    chapter = Chapter.objects.get(num=chapter_num, book=book)
    objs = chapter.comment_set.all()
    result = []
    for obj in objs:
        _get_comment_data(result, obj)
    
    return ajax.ajax_ok(result)
    
def chapter_num_comments(request, book_id, chapter_num, comment_num):
    book = Book.objects.get(pk=int(book_id))
    chapter = Chapter.objects.get(num=chapter_num, book=book)
    objs = chapter.comment_set.filter(comment_num=comment_num)
    result = []
    for obj in objs:
        _get_comment_data(result, obj)
    
    return ajax.ajax_ok(result)
