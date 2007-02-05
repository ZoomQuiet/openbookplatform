#coding=utf-8
from django.contrib.contenttypes.models import ContentType
from apps.comment.models import CommentInfo
from django.conf import settings
from utils import ajax
from utils.lib_page import Page
from utils import textconvert
from apps.comment.manipulator import EasyCommentManipulator

def _get_comment_data(request, obj, n):
    if obj.modifytime:
        modifytime = obj.modifytime.strftime("%Y-%m-%d %H:%S:%M")
    else:
        modifytime = ''
    return {'num':n+1, 'id':obj.id, 'title':obj.title, 'user_name':obj.user.username,
        'user_portrait':obj.user.userprofile.get_portrait(), 'user_id':obj.user.id,
        'createtime':obj.createtime.strftime("%Y-%m-%d %H:%S:%M"),
        'modifytime':modifytime, 'score':obj.score, 'content':textconvert.plaintext2html(obj.content)}

def list(request, model, object_id):
    """
    return model_object_id comments

    ajax_ok_data(curpageno, totalpagesnum, totalrecordnum, result)
    """
    cur = 0
    pages = 0
    totalcount = 0
    result = []
    ctype = ContentType.objects.get_for_model(model)
    try:
        info = CommentInfo.objects.get(content_type__pk=ctype.id, object_id=int(object_id))
    except CommentInfo.DoesNotExist:
        return ajax.ajax_ok_data((cur, pages, totalcount, result))
    pagenum = settings.COMMENT_PAGENUM
    objs = info.comment_set.all()
    totalcount = info.count
    if pagenum > 0:
        page = Page(objs, request, paginate_by=pagenum)
        cur = page.page
        object_list = page.object_list
        pages = (totalcount + pagenum - 1) / pagenum
    else:
        pagenum = 0
        object_list = objs
    for i, o in enumerate(object_list):
        result.append(_get_comment_data(request, o, i+(cur-1)*pagenum))
    return ajax.ajax_ok_data((cur, pages, totalcount, result))
    
def addcomment(request, owner_model, owner_id, model, object_id):
    owner = owner_model.objects.get(pk=int(owner_id))
    target = model.objects.get(pk=int(object_id))
    m = EasyCommentManipulator(request.user, content_object=target, owner_object=owner)
    f, obj = m.validate_and_save(request)
    if f:
        return ajax.ajax_ok(message="发布成功")
    return ajax.ajax_fail(obj)
