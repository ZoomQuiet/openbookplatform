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
import re
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.contrib.comments import CommentForm
from doc_trans.models import *

#@login_required
def index(request):
    project_objects = Project.objects.filter(suspended = False, versions__isnull = False).distinct().order_by('name')
    projects = []
    if request.user.is_authenticated():
        joined_projects = project_objects.filter(translators = request.user)
    else:
        joined_projects = []
    for project in project_objects:
        joined = project in joined_projects
        projects.append((project, joined))
    title = _(u"Project List")
    versions = Version.objects.order_by('-created').select_related()[:10]
    
    translators = User.objects.annotate(num_translations=Count('translations')).order_by('-num_translations').filter(num_translations__gt = 0)[:10]
    
    return render_to_response('doc_trans/trans/index.html',locals(), context_instance = RequestContext(request))

#@login_required
def project_page_list(request, slug, path = None):
    project_object = get_object_or_404(Project, slug = slug)
    versions = Version.objects.filter(project = project_object).order_by('-created').select_related()[:10]
    content = project_object.page_contents(path)
    
    if path:
        title = _(u"%s | Documentation Pages") % (project_object.name + ' | ' + ' | '.join(p for p in path.split('/') if p))
        path_sections = [p for p in path.split('/') if p]
    else:
        title = _(u"%s | Documentation Pages") % project_object
    
    user_joined = request.user in project_object.translators.all()

    return render_to_response('doc_trans/trans/project_page_list.html',locals(), context_instance = RequestContext(request))

#@login_required
def project_versions(request, slug):
    project_object = get_object_or_404(Project, slug = slug)
    user_joined = request.user in project_object.translators.all()
    versions = Version.objects.filter(project = project_object).order_by('-created').select_related()
    title = _(u"Versions of project %s") % project_object
    return render_to_response('doc_trans/trans/project_versions.html',locals(), context_instance = RequestContext(request))

#@login_required
def handle_comments(request, comment_object):
    if request.method == 'POST':
        data = request.POST.copy()
        if request.user.is_authenticated():
            data["name"] = request.user.get_full_name() or request.user.username
            data["email"] = request.user.email
        form = CommentForm(comment_object, data)
        if form.is_valid():
            comment = form.get_comment_object()
            comment.ip_address = request.META.get("REMOTE_ADDR", None)
            if request.user.is_authenticated():
                comment.user = request.user
            comment.save()
#            return HttpResponseRedirect('.')
    else:
        form = CommentForm(comment_object)
    return form

#@login_required
def project_comments(request, slug):
    project_object = get_object_or_404(Project, slug = slug)
    form = handle_comments(request, project_object)
    if form.is_valid():
        return HttpResponseRedirect('.')
    user_joined = request.user in project_object.translators.all()
    title = _(u"Comments of project %s") % project_object
    return render_to_response('doc_trans/trans/project_comments.html',locals(), context_instance = RequestContext(request))

#@login_required
def page_comments(request, project_slug, page_slug):
    project_object = get_object_or_404(Project, slug = project_slug)
    page_object = get_object_or_404(Page, project = project_object, slug = page_slug)
    form = handle_comments(request, page_object)
    if form.is_valid():
        return HttpResponseRedirect('.')
    user_joined = request.user in project_object.translators.all()
    title = _(u"Comments of page %s") % page_object.path
    return render_to_response('doc_trans/trans/page_comments.html',locals(), context_instance = RequestContext(request))

#@login_required
def paragraph_comments(request, paragraph_id):
    paragraph_object = get_object_or_404(Paragraph, id = paragraph_id)
    page_object = paragraph_object.page
    project_object = page_object.project
    form = handle_comments(request, paragraph_object)
    if form.is_valid():
        return HttpResponseRedirect('.')
    user_joined = request.user in project_object.translators.all()
    title = _(u"Comments of paragraph #%(ordinal)s, page %(page)s") % {'ordinal':paragraph_object.ordinal, 'page':page_object}
    return render_to_response('doc_trans/trans/paragraph_comments.html',locals(), context_instance = RequestContext(request))


#@login_required
def project_version(request, slug, revision):
    pass
#    not used


@login_required
def project_join_quit(request, slug, action):
    project_object = get_object_or_404(Project, slug = slug)
    joined = request.user in project_object.translators.all()
    
    if (action=='join' and joined) or (action=='quit' and not joined):
        return HttpResponseRedirect(project_object.page_list_url)
    
    if request.method == 'POST':
        if action=='join':
            project_object.translators.add(request.user)
            request.user.message_set.create(message=_(u'You have joined in project %s') % (project_object.name))
        elif action=='quit':
            project_object.translators.remove(request.user)
            request.user.message_set.create(message=_(u'You have quited project %s') % (project_object.name))
        return HttpResponseRedirect(request.POST['next'])
    next = request.META.get('HTTP_REFERER', project_object.page_list_url)
    title = _(u"Confirmation of %(action)s Project %(project)s") % {'action': action.title(), 'project': project_object.name}
    return render_to_response('doc_trans/trans/project_join_quit.html',locals(), context_instance = RequestContext(request))

review_name_re = re.compile(r'^reviewed-(\d+)$')
review_name_before_re = re.compile(r'^reviewed-(\d+)-before$')
#@login_required
def page_trans(request, project_slug, page_slug):
    if request.method == 'POST':
        reviewed = []
        before_status = {}
        now = datetime.datetime.now()
        for k,v in request.POST.items():
            m = review_name_re.match(k)
            if m:
                reviewed.append(int(m.group(1)))
            m = review_name_before_re.match(k)
            if m:
                before_status[int(m.group(1))] = int(v)
        for t_id,b_status in before_status.items():
            changed = (b_status == 0 and t_id in reviewed) or (b_status == 1 and t_id not in reviewed)
            if changed:
                translation_object = get_object_or_404(Translation, id = t_id)
                translation_object.reviewed = not translation_object.reviewed
                translation_object.reviewed_by = request.user
                translation_object.reviewed_at = now
                translation_object.save()
                request.user.message_set.create(message = _("Review status for paragraph #%s changed successfully.") % translation_object.paragraph.ordinal)
        return HttpResponseRedirect('.')
    
    project_object = get_object_or_404(Project, slug = project_slug)
    page_object = get_object_or_404(Page, project = project_object, slug = page_slug)
    user_joined = request.user in project_object.translators.all()
    paragraph_objects = page_object.current_paragraphs.order_by('ordinal').select_related(depth=1)
    paragraphs = paragraph_objects
    title = _("Translating Page %s") % page_object.path
    return render_to_response('doc_trans/trans/page_trans.html',locals(), context_instance = RequestContext(request))

#@login_required
def page_changes(request, project_slug, page_slug):
    project_object = get_object_or_404(Project, slug = project_slug)
    page_object = get_object_or_404(Page, project = project_object, slug = page_slug)
    user_joined = request.user in project_object.translators.all()
    paragraph_objects = page_object.current_paragraphs.order_by('ordinal')
    paragraphs = paragraph_objects
    title = _("Changes of page %s") % page_object.path
    return render_to_response('doc_trans/trans/page_changes.html',locals(), context_instance = RequestContext(request))

#@login_required
def page_version_changes(request, project_slug, page_slug, revision):
    project_object = get_object_or_404(Project, slug = project_slug)
    page_object = get_object_or_404(Page, project = project_object, slug = page_slug)
    user_joined = request.user in project_object.translators.all()
    page_change_object = get_object_or_404(PageChange, page = page_object, version__revision = revision)
    title = _("Changes of Page %(page)s at Version %(version)s") % {'page': page_object.path, 'version': revision}
    paragraphs = page_change_object.paragraphs.order_by('ordinal')
    return render_to_response('doc_trans/trans/page_version_changes.html',locals(), context_instance = RequestContext(request))


@login_required
@require_POST
def paragraph_translation(request, paragraph_id):
    paragraph = get_object_or_404(Paragraph, id = paragraph_id)
    if request.method == 'POST':
#        print request.POST
        content = request.POST.get('new_content').strip()
        if content:
            new_translation = Translation(paragraph = paragraph, history_translation = paragraph.latest_translation,
                                          translator = request.user, content = content, ip = request.META.get('REMOTE_ADDR',''))
            new_translation.save()
            
            paragraph.page.re_build_translation()
            
            return render_to_response('doc_trans/trans/paragraph_translation.html',locals())
        else:
            content = request.POST.get('old_content').strip()
            return render_to_response('doc_trans/trans/paragraph_translation.html',locals())
    
#@login_required
def paragraph_histories(request, paragraph_id):
    paragraph_object = get_object_or_404(Paragraph, id = paragraph_id)
    page_object = paragraph_object.page
    project_object = page_object.project
    latest_translation = paragraph_object.latest_translation
    user_joined = request.user in project_object.translators.all()
    title = _("Changes of paragraph #%s") % paragraph_object.ordinal
    paragraphs = paragraph_object.history_paragraphs
    
    return render_to_response('doc_trans/trans/paragraph_histories.html',locals(), context_instance = RequestContext(request))

#@login_required
def paragraph_translation_histories(request, paragraph_id):
    paragraph_object = get_object_or_404(Paragraph, id = paragraph_id)
    page_object = paragraph_object.page
    project_object = page_object.project
    latest_translation = paragraph_object.latest_translation
    user_joined = request.user in project_object.translators.all()
    title = _("Translation Changes of paragraph #%s") % paragraph_object.ordinal
    translations = latest_translation.history_translations
    
    return render_to_response('doc_trans/trans/paragraph_translation_histories.html',locals(), context_instance = RequestContext(request))

    
#@login_required
def people_list(request):
    people_objects = User.objects.annotate(num_translations=Count('translations')).order_by('-num_translations').filter(num_translations__gt = 0)

    page_num = int(request.GET.get('page_num','1'))
    p = Paginator(people_objects, 100)
    current_page = p.page(page_num)
    current_people_list = current_page.object_list
    
    title = _("People List")
    
    return render_to_response('doc_trans/trans/people_list.html',locals(), context_instance = RequestContext(request))

#@login_required
def people(request, username):
    user_object = get_object_or_404(User, username = username)
    joined_projects = user_object.joined_projects.order_by('name')

    translations = user_object.translations.filter(modified_translation = None).order_by('-created')
    
    selectd_project_slug = request.GET.get('project','')
    if selectd_project_slug:
        selectd_project_object = get_object_or_404(Project, slug = selectd_project_slug)
        translations = translations.filter(paragraph__page__project = selectd_project_object)
        page_contents = selectd_project_object.page_contents()
        
    selectd_page_slug = request.GET.get('page','')
    if selectd_page_slug:
        selectd_page_object = get_object_or_404(Page, project = selectd_project_object, slug = selectd_page_slug)
        translations = translations.filter(paragraph__page = selectd_page_object)
        
    page_num = int(request.GET.get('page_num','1'))
    p = Paginator(translations, 10)
    current_page = p.page(page_num)
    translation_list = current_page.object_list
    
    title = _("Translations of People %s") % user_object
    
    return render_to_response('doc_trans/trans/people.html',locals(), context_instance = RequestContext(request))

def help(request):
    title = _("Help Center")
    return render_to_response('doc_trans/trans/help.html',locals(), context_instance = RequestContext(request))

def setlang(request):
    from django.views.i18n import set_language
    return set_language(request)
