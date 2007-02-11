#coding=utf-8
from django.contrib.auth.models import User
from utils import decorator
from apps.users.models import UserProfile

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

