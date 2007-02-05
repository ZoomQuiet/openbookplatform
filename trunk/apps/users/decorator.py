#coding=utf-8
from django.contrib.auth.models import User
from utils import decorator
from apps.users.models import UserProfile, Group
from apps.forum.models import Topic

def check_userprofile(func):
    def _func(*args, **kwargs):
        request = args[0]
        user = request.user
        try:
            profile = user.userprofile
        except:
            #if there is no profile record existed, then create a new record first
            profile = UserProfile(user=user)
            profile.save()
        return func(*args, **kwargs)
    return _func

def check_userid(f):
    """
    Check if the useid is existed
    """
    
    @decorator.exceptionhandle
    def _f(*args, **kwargs):
        request = args[0]
        object_id = kwargs['object_id']
        try:
            person = User.objects.get(pk=int(object_id))
        except User.DoesNotExist:
            raise Exception, "用户 ID (%s) 不存在！" % object_id
        return f(*args, **kwargs)
    return _f

def check_groupid(f):
    """
    Check if the groupid is existed
    """
    
    @decorator.exceptionhandle
    def _f(*args, **kwargs):
        request = args[0]
        print kwargs
        group_id = kwargs['group_id']
        try:
            group = Group.objects.get(pk=int(group_id))
        except Group.DoesNotExist:
            raise Exception, "小组 ID (%s) 不存在！" % group_id
        return f(*args, **kwargs)
    return _f

def add_person(f):
    def _f(*args, **kwargs):
        request = args[0]
        object_id = kwargs['object_id']
        person = User.objects.get(pk=int(object_id))
        result = f(*args, **kwargs)
        result['person'] = person
        return result
    return _f

def add_group(f):
    def _f(*args, **kwargs):
        request = args[0]
        object_id = kwargs.get('group_id', '') or kwargs.get('object_id', '')
        group = Group.objects.get(pk=int(object_id))
        result = f(*args, **kwargs)
        result['group'] = group
        return result
    return _f

def get_topic(f):
    def _f(request, group_id, topic_id, *args, **kwargs):
        return f(request, Topic, topic_id, *args, **kwargs)
    return _f

def get_owner_and_topic(f):
    def _f(request, group_id, topic_id, *args, **kwargs):
        return f(request, Group, group_id, Topic, topic_id, *args, **kwargs)
    return _f
