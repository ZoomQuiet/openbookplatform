#coding=utf-8
from utils.common import render_template
from django.contrib.auth.models import User

from utils import ajax
from apps.users.views.authvalidator import ChangeValidator

def user_detail(request, object_id):
    person = User.objects.get(pk=int(object_id))
    return render_template(request, 'users/user_detail.html', {'person':person})

def user_edit(request, object_id):
    if request.POST:
        v = ChangeValidator(request, object_id)
        f, obj = v.validate_and_save(request)
        if f:
            return ajax.ajax_ok(message=_('User infomation updated successful!'))
        return ajax.ajax_fail(obj)
    else:
        user = User.objects.get(pk=int(object_id))
        d = {'person':user}
        return render_template(request, 'users/user_edit.html', d)

