from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from apps.users.models import Group
from utils import ajax, decorator
from apps.users.manipulator import AdminGroupManipulator
import apps.users.decorator as ud

def group_list(request):
    objs = Group.objects.all()
    user = request.user
    m = AdminGroupManipulator(user)
    return render_to_response('users/group.html', context_instance=RequestContext(request, {'groups':objs, 'form':m.form()}))

def group_add(request):
    user = request.user
    m = AdminGroupManipulator(user)
    f, obj = m.validate_and_save(request)
    if f:
        return HttpResponseRedirect('/group/')
    
    objs = Group.objects.all()
    data, errors = request.POST.copy(), obj
    return render_to_response('users/group.html', context_instance=RequestContext(request, {'groups':objs, 'form':m.form(data, errors)}))
    
@ud.check_groupid
def group_detail(request, group_id):
    obj = Group.objects.select_related().get(pk=int(group_id))
    
    #set current group session
    request.session['group_id'] = obj.id
    
    user = request.user
    m = AdminGroupManipulator(user)
    return render_to_response('users/group_detail.html', context_instance=RequestContext(request, {'group':obj}))

@ud.check_groupid
def group_edit(request, group_id):
    user = request.user
    group = Group.objects.select_related().get(pk=int(group_id))
    m = AdminGroupManipulator(user, group_id)
    if request.POST:
        f, obj = m.validate_and_save(request)
        if f:
            return HttpResponseRedirect('/group/%s/edit/' % group_id)
        
        data, errors = request.POST.copy(), obj
        return render_to_response('users/group_edit.html', context_instance=RequestContext(request, {'group':data, 'form':m.form(data, errors)}))
    else:
        data = group.__dict__
        data['managers'] = group.get_managers()
        return render_to_response('users/group_edit.html', context_instance=RequestContext(request, {'group':group, 'form':m.form(data)}))

@ud.check_groupid
@decorator.redirect('/group/')
def group_delete(request, group_id):
    obj = Group.objects.get(pk=int(group_id))
    obj.delete()

@ud.check_groupid
def group_addmember(request, group_id):
    group = Group.objects.get(pk=int(group_id))
    members = request.POST['members']
    for m in members.split():
        try:
            user = User.objects.get(username=m)
        except User.DoesNotExist:
            pass
        else:
            group.add_member(user)
    return HttpResponseRedirect('/group/%s/edit/' % group_id)

@ud.check_groupid
def group_delmember(request, group_id, object_id):
    group = Group.objects.get(pk=int(group_id))
    
    try:
        user = User.objects.get(pk=int(object_id))
    except User.DoesNotExist:
        pass
    else:
        group.del_member(user)
    return HttpResponseRedirect('/group/%s/edit/' % group_id)

@ud.check_groupid
def group_join(request, group_id):
    group = Group.objects.get(pk=int(group_id))
    group.add_member(request.user)
    return HttpResponseRedirect('/group/%s/' % group_id)
    