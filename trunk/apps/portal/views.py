from django.shortcuts import render_to_response
from django.template.context import RequestContext

def index(request):
    return render_to_response('index.html', 
        context_instance=RequestContext(request))
        
def license(request):
    return render_to_response('license.html', 
        context_instance=RequestContext(request))
    
def login(request):
    if request.POST:
        from apps.users.views.auth import user_login
        return user_login(request)
    else:
        return render_to_response('users/user_login.html', 
            context_instance=RequestContext(request))
    