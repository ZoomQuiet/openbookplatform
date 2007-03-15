#coding=utf-8
from django.contrib.auth.models import User
from apps.books.models import Book, Chapter, Comment
from utils.lib_page import Page
from utils import ajax
from apps.books.validator import BookValidator, ChapterValidator
from utils.common import render_template, setting

def user_books(request, object_id):
    user = User.objects.get(pk=int(object_id))
    return render_template(request, 'users/user_book.html', {'person':user})

def _get_data(request, obj):
    if obj.icon:
        icon = '<img class="border" src="/site_media/%s" alt="%s"/>' % (obj.get_icon_url(), obj.title)
    else:
        icon = '<img class="border" src="/site_media/img/book_icon.jpg" alt="%s"/>' % obj.title
    authors = [x.username for x in obj.authors.all()]
    checkbox = '<input type="checkbox" name="book_id" value="%d"/>' % obj.id
    return ({'id':obj.id, 'icon':icon, 'title':obj.title, 
        'description':obj.description, 'author':','.join(authors),
        'checkbox':checkbox})

def user_books_list(request, object_id):
    #because filtermiddleware guarantee the url match with request.user
    #so here don't need to get the user object, but just using request.user
#    user = User.objects.get(pk=int(object_id))
    user = request.user
    pagenum = 10
    result = []
    #if the user is superuser, then all book will be shown
    if user.is_superuser:
        objs = Book.objects.all()
    else:
        objs = user.book_set.all()
    page = Page(objs, request, paginate_by=pagenum)
    for o in page.object_list:
        result.append(_get_data(request, o))
    pages = (objs.count() + pagenum - 1) / pagenum
    cur = int(request.GET.get('page', 1))
    return ajax.ajax_ok((cur, pages, result))
    
def user_books_delete(request, object_id):
    user = request.user
    ids = request.POST.getlist('book_id')
    if ids:
        for book in Book.objects.filter(id__in=ids):
            book.delete()
    return ajax.ajax_ok(_('Success!'))

def user_book_edit(request, object_id, book_id=None):
    user = request.user
    v = BookValidator(request, book_id)
    flag , obj = v.validate_and_save(request)
    if flag:
        return ajax.ajax_ok(_('Success!'))
    return ajax.ajax_fail(obj)

def user_book_detail(request, object_id, book_id):
    user = User.objects.get(pk=int(object_id))
    book = Book.objects.get(pk=int(book_id))
    return render_template(request, 'users/user_book_detail.html', 
        {'person':user, 'book':book})
    
def user_book_chapters(request, object_id, book_id):
    user = User.objects.get(pk=int(object_id))
    book = Book.objects.get(pk=int(book_id))
    objs = book.chapter_set.all()
    result = []
    def _get_data(request, obj):
        checkbox = '<input type="checkbox" name="chapter_id" value="%d"/>' % obj.id
        return ({'id':obj.id, 'chapter_num':obj.num, 'title':obj.title, 
            'abstract':obj.abstract, 'checkbox':checkbox, 'date':obj.modifydate.strftime("%b %d,%Y %I:%m %p")})
    for o in objs:
        result.append(_get_data(request, o))
    return ajax.ajax_ok(result)

def user_chapters_delete(request, object_id, book_id):
    ids = request.POST.getlist('chapter_id')
    if ids:
        for chapter in Chapter.objects.filter(id__in=ids):
            chapter.delete()
    return ajax.ajax_ok(next=setting('URLROOT') + '/user/%s/book/%s/' % (object_id, book_id))

def user_chapter(request, object_id, book_id, chapter_id=None):
    if request.GET:
        o = Chapter.objects.get(pk=int(chapter_id))
        result = {'id':o.id, 'content':o.content, 'abstract':o.abstract,
            'title':o.title, 'date':o.modifydate.strftime("%b %d,%Y %I:%m %p")}
        return ajax.ajax_ok(result)
    else:
        v = ChapterValidator(request, book_id, chapter_id)
        if request.POST:
            flag, obj = v.validate_and_save(request)
            if flag:
                return ajax.ajax_ok(message=_("Success!"))
            return ajax.ajax_fail(obj, message=_("There are some errors!"))
        else:
            user = User.objects.get(pk=int(object_id))
            book = Book.objects.get(pk=int(book_id))
            chapter = Chapter.objects.get(pk=int(chapter_id))
            return render_template(request, 'users/user_chapter.html', 
                {'person':user, 'book':book, 'chapter':chapter})
            
def user_book_authors(request, object_id, book_id):
    book = Book.objects.get(pk=int(book_id))
    result = []
    for obj in book.authors.all():
        result.append({'username':obj.username})
    return ajax.ajax_ok(result)

from apps.books.validator import AddUserValidator
def user_book_addauthor(request, object_id, book_id):
    v = AddUserValidator(book_id)
    flag, obj = v.validate_and_save(request)
    if flag:
        return ajax.ajax_ok()
    return ajax.ajax_fail(obj)
    
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
    html = '<a class="delete" href="#">[X]</a> %s %s:[%s] %s' % (status, username, obj.comment_num, content)
#    result.append({'username':username,
#        'content':plaintext2html(obj.content), 'status':status,
#        'createtime':obj.createtime.strftime("%b %d,%Y %I:%m %p")})
    result.append({'html':html, 'id':obj.id})

def user_chapter_comments(request, object_id, book_id, chapter_id):
    chapter = Chapter.objects.get(pk=int(chapter_id))
    objs = chapter.comment_set.all().order_by('comment_num', 'createtime')
    result = []
    for obj in objs:
        _get_comment_data(result, obj)
    
    return ajax.ajax_ok(result)
    
def user_chapter_delcomment(request, object_id, book_id, chapter_id):
    obj = Comment.objects.get(pk=int(request.POST['comment_id']))
    obj.delete()
    return ajax.ajax_ok(message='ok')