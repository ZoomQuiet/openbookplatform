# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django import forms
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Count
import os
from django.contrib.auth.decorators import login_required
from doc_trans.models import *
from doc_trans.utils import get_url_handler
from doc_trans.trans_views import index

def project_list(request):
    return index(request)

#    project_objects = Project.objects.filter(suspended = False, versions__isnull = False).distinct().order_by('name')
#    projects = project_objects
#    title = _(u"Project List")
#    versions = Version.objects.order_by('-created').select_related()[:10]
#    translators = User.objects.annotate(num_translations=Count('translations')).order_by('-num_translations').filter(num_translations__gt = 0)[:10]
#    return render_to_response('doc_trans/project_list.html',locals(), context_instance = RequestContext(request))

def project_index(request, project_slug):
    
    return render_to_response('doc_trans/project_index.html',locals(), context_instance = RequestContext(request))

def project_serve(request, project_slug, path):
    if len(path.split('/')) == 1:
        return HttpResponseRedirect(request.path + '/')

    project_object = get_object_or_404(Project, slug = project_slug)
    url_handler = get_url_handler(project_object)
    return url_handler.serve(request, project_object, path)
    