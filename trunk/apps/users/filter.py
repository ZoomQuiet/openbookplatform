from django.contrib.auth.models import User
from utils.common import render_template

def check_valid_user(request, user_id):
    if request.user.is_anonymous():
        return render_template(request, 'users/user_login.html', {'next':'%s' % request.path})
    try:
        person = User.objects.get(pk=int(user_id))
    except User.DoesNotExist:
        return render_template(request, 'error.html', {'message':_("User ID (%s) is not existed!") % user_id})
    if person.id != request.user.id:
        return render_template(request, 'error.html', {'message':_('You have no right to view the page!')})
