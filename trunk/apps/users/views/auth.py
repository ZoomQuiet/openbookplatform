import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction

from utils import ajax
from utils import decorator
from apps.users.views.authvalidator import LoginValidator, RegisterValidator
from utils.common import render_template, setting

def user_login(request):
    v = LoginValidator()
    f, result = v.validate(request)
    if not f:
        return ajax.ajax_fail(result)
    
    username = result['username']
    password = result['password']
    user = authenticate(username=username, password=password)
    if user is None:
        message = {'_':_('Authentication is failed!')}
        if '@' in username:
            # Mistakenly entered e-mail address instead of username? Look it up.
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                message['username'] = _("Usernames cannot contain the '@' character.")
            else:
                message['username'] = _("Your e-mail address is not your username. Try '%s' instead.") % user.username
        return ajax.ajax_fail(message)
    
    # The user data is correct; log in the user in and continue.
    else:
        if user.is_staff:
            login(request, user)
            user.last_login = datetime.datetime.now()
            user.save()
        return ajax.ajax_ok(True, next=request.POST.get('next', setting('URLROOT') + '/'))

from django.dispatch import dispatcher
import apps.users.signals

@decorator.redirect(setting('URLROOT') + '/')                
def user_logout(request):
    dispatcher.send(signal=apps.users.signals.user_logout, request=request)
    logout(request)

@transaction.autocommit
def user_register(request):
    v = RegisterValidator(request)
    if request.POST:
        f, obj = v.validate_and_save(request)
        if f:
            user = authenticate(username=obj.username, password=obj.password)
            if user and user.is_staff:
                login(request, user)
                user.last_login = datetime.datetime.now()
                user.save()
            return ajax.ajax_ok(True, next=setting('URLROOT') + '/')
        return ajax.ajax_fail(obj)
    else:
        return render_template(request, 'users/register.html')
