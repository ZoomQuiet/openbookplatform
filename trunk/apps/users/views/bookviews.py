from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from apps.books.models import Book, Chapter
from utils.lib_page import Page
from utils import ajax
from apps.books.manipulator import BookManipulator, ChapterManipulator

def user_books(request, object_id):
    user = User.objects.get(pk=int(object_id))
    return render_to_response('users/user_book.html', 
        context_instance=RequestContext(request, {'person':user}))

def _get_data(request, obj):
    if obj.icon:
        icon = '<img src="/site_media/%s" alt="%s"/>' % (obj.get_icon_url(), obj.title)
    else:
        icon = '<img src="/site_media/img/book_icon.jpg" alt="%s"/>' % obj.title
    authors = [x.username for x in obj.authors.all()]
    checkbox = '<input type="checkbox" name="book_id" value="%d"/>' % obj.id
    return ({'id':obj.id, 'icon':icon, 'title':obj.title, 
        'description':obj.description, 'author':','.join(authors),
        'checkbox':checkbox})

def user_books_list(request, object_id):
    user = User.objects.get(pk=int(object_id))
    pagenum = 10
    result = []
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
    m = BookManipulator(request, book_id)
    flag , obj = m.validate_and_save(request)
    if flag:
        return ajax.ajax_ok(_('Success!'))
    return ajax.ajax_fail(obj)

def user_book_detail(request, object_id, book_id):
    user = User.objects.get(pk=int(object_id))
    book = Book.objects.get(pk=int(book_id))
    return render_to_response('users/user_book_detail.html', 
        context_instance=RequestContext(request, {'person':user, 'book':book}))
    
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
    return ajax.ajax_ok(next='/user/%s/book/%s/' % (object_id, book_id))

def user_chapter(request, object_id, book_id, chapter_id=None):
    if request.GET:
        o = Chapter.objects.get(pk=int(chapter_id))
        result = {'id':o.id, 'content':o.content, 'abstract':o.abstract,
            'title':o.title, 'date':o.modifydate.strftime("%b %d,%Y %I:%m %p")}
        return ajax.ajax_ok(result)
    else:
        m = ChapterManipulator(request, book_id, chapter_id)
        if request.POST:
            flag, obj = m.validate_and_save(request)
            if flag:
                return ajax.ajax_ok(message=_("Success!"))
            return ajax.ajax_fail(obj, message=_("There are some errors!"))
        else:
            user = User.objects.get(pk=int(object_id))
            book = Book.objects.get(pk=int(book_id))
            chapter = Chapter.objects.get(pk=int(chapter_id))
            return render_to_response('users/user_chapter.html', 
                context_instance=RequestContext(request, {'person':user, 'book':book, 'chapter':chapter}))
            