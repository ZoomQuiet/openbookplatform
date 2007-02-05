#coding=utf-8
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from utils import ajax
from apps.users.manipulator import UserEditManipulator, UserPortraitManipulator
import apps.users.decorator as ud

@ud.check_userid
@ud.check_userprofile
def user_detail(request, object_id):
    person = User.objects.get(pk=int(object_id))
    return render_to_response('users/user_detail.html', context_instance=RequestContext(request, {'person':person}))

@ud.check_userid
@ud.check_userprofile
def user_edit(request, object_id):
    user = User.objects.get(pk=int(object_id))
    
    m1 = UserEditManipulator(request, object_id)
    if request.POST:
        f, obj = m1.validate_and_save(request)
        if f:
            return ajax.ajax_ok(message="用户信息已经被更新")
        return ajax.ajax_fail(obj)
    else:
        data = user.__dict__
        data['password'] = ''
        m2 = UserPortraitManipulator(request, user)
        d = {'baseform':m1.form(data), 'photoform':m2.form(), 'person':user}
        return render_to_response('users/user_edit.html', context_instance=RequestContext(request, d))

@ud.check_userid
def user_save_portrait(request, object_id):
    user = User.objects.get(pk=int(object_id))
    m2 = UserPortraitManipulator(request, user)
    f, obj = m2.validate_and_save(request)
    if f:
        return HttpResponseRedirect('/user/%s/edit/' % object_id)
    
    data, errors = user.__dict__, {}
    data['password'] = ''
    m1 = UserEditManipulator(request)
    d = {'baseform':m1.form(data, errors), 'photoform':m2.form(None, obj), 'person':user}
    return render_to_response('users/user_edit.html', context_instance=RequestContext(request, d))

def userlist(request):
    users = User.objects.all()
    return render_to_response('users/list.html', context_instance=RequestContext(request, {'users':users}))

def user_delete_multi(request):
    user_id = request.POST.getlist('userid')
    User.objects.filter(id__in=user_id).delete()
    return ajax.ajax_ok(next='/user/')

@ud.check_userid
def user_delete(request, object_id=None):
    if object_id:
        User.objects.get(pk=int(object_id)).delete()
        return HttpResponseRedirect('/user/')

def user_addsysmanager_multi(request):
    user_id = request.POST.getlist('userid')
    for u in User.objects.filter(id__in=user_id):
        u.is_superuser = True
        u.save()
    return ajax.ajax_ok(next='/user/')

@ud.check_userid
def user_addsysmanager(request, object_id=None):
    person = User.objects.get(pk=int(object_id))
    person.is_superuser = True
    person.save()
    return HttpResponseRedirect('/user/%s/' % object_id)
    
@ud.check_userid
def user_removesysmanager(request, object_id):
    person = User.objects.get(pk=int(object_id))
    if person.username != 'admin':
        person.is_superuser = False
        person.save()
    return HttpResponseRedirect('/user/%s/' % object_id)
