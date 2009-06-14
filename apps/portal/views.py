from utils.common import render_template
from django.template.context import RequestContext

def index(request):
    return render_template(request, 'index.html')
        
def license(request):
    return render_template(request, 'license.html')
   
def help(request):
    return render_template(request, 'help.html')

def login(request):
    if request.POST:
        from apps.users.views.auth import user_login
        return user_login(request)
    else:
        return render_template(request, 'users/user_login.html')
    
