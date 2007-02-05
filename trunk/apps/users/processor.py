from models import Group

def groupinfo(request):
    group = None
    if request.session.get('group_id', ''):
        group_id = request.session['group_id']
        try:
            group = Group.objects.get(pk=int(group_id))
        except:
            pass
    return {'lastgroup':group}

from django.dispatch import dispatcher
import apps.users.signals

def remove_group_session(signal, sender, request):
    if request.session.get('group_id', ''):
        request.session['group_id'] = None
        
dispatcher.connect(remove_group_session, signal=apps.users.signals.user_logout)