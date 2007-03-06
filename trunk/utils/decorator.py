class HttpRedirectException(Exception):pass

# Ajax process decorator
import ajax

def json(func):
    """
    Encapsulate data into json format, and call HttpResponse to reture
    """
    @exceptionhandle
    def _f(*args, **kwargs):
        result = func(*args, **kwargs)
        return ajax.json_response(result)
    return _f

# render_template
from utils.common import render_template
from django.http import HttpResponseRedirect

def template(templatename):
    """
    render the func's result into a template
    """
    
    def _render(func=None):
        @exceptionhandle
        def _f(request, *args, **kwargs):
            if func:
                result = func(request, *args, **kwargs)
            else:
                result = {}
            return render_template(request, templatename, result)
        return _f
    return _render

from django.conf import settings

def exceptionhandle(func):
    """
    Catch Special Exception and deal with them
    """
    def _f(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except HttpRedirectException, e:
            return HttpResponseRedirect(str(e))
    return _f

def errorhandle(func):
    """
    Catch Exception and show it in a error page, or redirect to new url
    """
    def _f(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception, e:
            if settings.DEBUG:
                import traceback
                traceback.print_exc()
            request.session['_errormsg'] = str(e)
            return HttpResponseRedirect('/error/')
    return _f
    
def redirect(url):
    """
    Redirect to another url after calling a function
    """
    def _redirect(func):
        def _f(request, *args, **kwargs):
            result = func(request, *args, **kwargs)
            return HttpResponseRedirect(url)
        return _f
    return _redirect

def debug(func):
    """
    Catch Exception and show it in a error page
    """
    def _f(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception, e:
            import traceback
            traceback.print_exc()
            raise
    return _f

#from utils.deco import decorator as deco
#def validate(validateClass, return_error=True, error_message=_('There are some errors!')):
#    def _f(func, request, *args, **kwargs):
#        if request.method == 'POST':
#            v = validateClass
#            if hasattr(v, '__bases__'):  #class type
#                from utils.common import get_func_args
#                f = getattr(v, '__init__', None)
#                if f:
#                    args, kwargs = get_func_args(f, args, kwargs, skip=1)
#                    v_obj = v(*args, **kwargs)
#                else:
#                    v_obj = v()
#            else:
#                v_obj = v
#            flag, result = v_obj.validate(request)
#            request.validator_obj = v_obj
#            if flag:
#                request.DATA = result
#                request.ERROR = None
#            else:
#                request.ERROR = result
#                request.DATA = None
#            if return_error and request.ERROR:
#                return ajax.ajax_fail_data(result, message=error_message)
#        return deco(func(request, *args, **kwargs))
#    return _f