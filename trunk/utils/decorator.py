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
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

def template(templatename):
    """
    render the func's result into a template
    """
    
    def _render(func=None):
        @exceptionhandle
        def _f(*args, **kwargs):
            if func:
                result = func(*args, **kwargs)
            else:
                result = {}
            return render_to_response(templatename, context_instance=RequestContext(args[0], result))
        return _f
    return _render

from django.conf import settings

def exceptionhandle(func):
    """
    Catch Special Exception and deal with them
    """
    def _f(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HttpRedirectException, e:
            return HttpResponseRedirect(str(e))
    return _f

def errorhandle(func):
    """
    Catch Exception and show it in a error page, or redirect to new url
    """
    def _f(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, e:
            if settings.DEBUG:
                import traceback
                traceback.print_exc()
            request = args[0]
            request.session['_errormsg'] = str(e)
            return HttpResponseRedirect('/error/')
    return _f
    
def redirect(url):
    """
    Redirect to another url after calling a function
    """
    def _redirect(func):
        def _f(*args, **kwargs):
            result = func(*args, **kwargs)
            return HttpResponseRedirect(url)
        return _f
    return _redirect

def debug(func):
    """
    Catch Exception and show it in a error page
    """
    def _f(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, e:
            import traceback
            traceback.print_exc()
            raise
    return _f
  
def ajax_iframe_response(func):
    """
    """
    def _f(*args, **kwargs):
        a = '''<script type="text/javascript">
  window.parent.ajax_iframe_response(%r);
</script>'''
        return HttpResponse(a % ajax.json(func(*args, **kwargs)))
    return _f

