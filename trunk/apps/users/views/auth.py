import datetime

from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from apps.users.manipulator import UserRegisterManipulator
from django.template.context import RequestContext

from utils import ajax
from utils import decorator

def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
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
        return ajax.ajax_ok(True, next='/')

from django.dispatch import dispatcher
import apps.users.signals

@decorator.redirect('/')                
def user_logout(request):
    dispatcher.send(signal=apps.users.signals.user_logout, request=request)
    logout(request)

@transaction.autocommit
def user_register(request):
    m = UserRegisterManipulator(request)
    if request.POST:
        f, obj = m.validate_and_save(request)
        if f:
            user = authenticate(username=obj.username, password=obj.password)
            if user and user.is_staff:
                login(request, user)
                user.last_login = datetime.datetime.now()
                user.save()
            return ajax.ajax_ok(True, next='/')
        return ajax.ajax_fail(obj)
    else:
        return render_to_response('users/register.html', context_instance=RequestContext(request, {'form':m.form()}))
