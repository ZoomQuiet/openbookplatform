from django.http import HttpResponseRedirect

def next_url(request, url, direct_string='next'):
    next_url = request.REQUEST.get(direct_string, '')
    if not next_url:
        next_url = url
    return next_url

def next_redirect(request, url, direct_string='next'):
    return HttpResponseRedirect(next_url(request, url, direct_string))