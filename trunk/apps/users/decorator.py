#coding=utf-8
from django.contrib.auth.models import User
from utils import decorator
from apps.users.models import UserProfile
from utils.common import render_template

def check_userprofile(func):
    def _func(request, *args, **kwargs):
        user = request.user
        try:
            profile = user.userprofile
        except:
            #if there is no profile record existed, then create a new record first
            profile = UserProfile(user=user)
            profile.save()
        return func(request, *args, **kwargs)
    return _func

def check_userid(f):
    """
    Check if the useid is existed
    """
    
    @decorator.exceptionhandle
    def _f(request, *args, **kwargs):
        object_id = kwargs['object_id']
        try:
            person = User.objects.get(pk=int(object_id))
        except User.DoesNotExist:
            raise Exception, "用户 ID (%s) 不存在！" % object_id
        return f(request, *args, **kwargs)
    return _f

def check_valid_user(f):
    """
    Check if the useid is valid
    """
    
    def _f(request, *args, **kwargs):
        if request.user.is_anonymous():
            return render_template(request, 'users/user_login.html', {'next':'%s' % request.path})
        object_id = kwargs['object_id']
        try:
            person = User.objects.get(pk=int(object_id))
        except User.DoesNotExist:
            return render_template(request, 'error.html', {'message':_("User ID (%s) is not existed!") % object_id})
        if person.id != request.user.id:
            return render_template(request, 'error.html', {'message':_('You have no right to view the page!')})
        return f(request, *args, **kwargs)
    return _f
