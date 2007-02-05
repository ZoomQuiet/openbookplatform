from django.conf import settings
from utils import join_path
from django.shortcuts import render_to_response
from apps.site.models import BlogSite

def get_app_root(appname, host='main'):
    hosturl = settings.HOST_URL.get(host, '')
    return join_path(hosturl, settings.APP_ROOT.get(appname, ''))

def get_model(model_name):
    from django.db import models
    app_model = settings.MODEL_NAMES.get(model_name, None)
    if app_model:
        return models.get_model(*app_model)
    else:
        return None
    
def get_template_theme_root(user=None):
    if get_current_theme(user):
        return getattr(settings, 'TEMPLATE_THEME_ROOT', '')
    else:
        return ''

def get_media_theme_root(user=None):
    if get_current_theme(user):
        return getattr(settings, 'MEDIA_THEME_ROOT', '')
    else:
        return ''

def join_app_path(appname, *args, **kwargs):
    if kwargs.has_key('host'):
        host = kwargs.get('host')
    else:
        host = 'main'
    return join_path(get_app_root(appname, host), *args)

def get_current_theme(user=None):
    if not user:
        sites = BlogSite.objects.all()
        if len(sites) == 0:
            return ''
        else:
            site = sites[0]
            return site.themename
    else:
        return user.userprofile.themename
    
def theme_template(template_name, user=None):
    if not isinstance(template_name, (list, tuple)):
        template_name = [template_name]
    t = [join_path('%s/%s' % (get_template_theme_root(user), get_current_theme(user)), f) for f in template_name]
    return t + template_name

def theme_render_to_response(args, user=None, **kwargs):
    return render_to_response(theme_template(args, user), **kwargs)

def theme_media_root(themename, funcname, user=None, medias='medias'):
    return join_path(get_app_root(medias), get_media_theme_root(user), funcname, themename)
