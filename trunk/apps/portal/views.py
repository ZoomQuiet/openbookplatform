from django.shortcuts import render_to_response
from django.template.context import RequestContext
from utils import decorator

def index(request):
    return render_to_response('index.html', 
        context_instance=RequestContext(request))
        
def license(request):
    return render_to_response('license.html', 
        context_instance=RequestContext(request))
    
@decorator.template('error.html')
def error(request):
    emsg = request.session['_errormsg']
    return {'errormsg':emsg}