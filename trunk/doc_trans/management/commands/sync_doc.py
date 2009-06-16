# -*- coding: utf-8 -*-
import os
import sys
from optparse import make_option

from django.core.management.base import LabelCommand, CommandError
from django.utils.importlib import import_module
from django.db import transaction
from django.core.exceptions import ValidationError
from doc_trans.models import Project, Page, Paragraph, Translation, Version, PageChange
from doc_trans.utils import get_file_handler, get_simple_path
import pysvn

min_similarity = 0.7

            
def handle_page_added(project, added_version, page_path, page_simple_path):
    page = Page.objects.create(project = project, path = page_simple_path, current_version = added_version)
    print "created page '%s' for path '%s' at version '%s'" % (page.slug, page.path, added_version.revision)
    
    page_change = PageChange.objects.create(version = added_version, page = page, action = 'added')
    print "created page_change '%s' for page '%s'" % (page_change.action, page_change.page.path, )
    
    file_handler = get_file_handler(page)
    page_content = open(page_path).read()
    paragraphs = file_handler.split(page_content, file_name = page_path)
    for ordinal, paragraph_content in enumerate(paragraphs):
        paragraph = Paragraph.objects.create(page = page, current_version = added_version,
                                             original = paragraph_content, ordinal = ordinal + 1)
#        print "created paragraph '%s' for page '%s'" % (paragraph.ordinal, paragraph.page.path, )
    page.check()
    print

def handle_page_deleted(project, before_version, deleted_version, page_path, page_simple_path):
    page = Page.objects.get(project = project, path = page_simple_path, current_version = before_version)
    print "found page '%s' for path '%s' at before_version '%s'" % (page.slug, page.path, page.current_version.revision)
    page.deleted = True
    page.current_version = deleted_version
    page.save()
    print "deleted page '%s' for path '%s' at deleted_version '%s'" % (page.slug, page.path, page.current_version.revision)
    
    page_change = PageChange.objects.create(version = deleted_version, page = page, action = 'deleted')
    print "created page_change '%s' for page '%s'" % (page_change.action, page_change.page.path, )
    
    paragraphs = page.paragraphs.filter(current_version = before_version)
    print "found '%s' paragraphs(ids:%s) for page '%s' will be deleted" % (paragraphs.count(), u",".join(str(p.id) for p in paragraphs), page.path)
    for p in paragraphs:
        p.current_version = deleted_version
        p.save()
    
    print

def handle_page_modified(project, before_version, modified_version, page_path, page_simple_path):
    page = Page.objects.get(project = project, path = page_simple_path, current_version = before_version)
    print "found page '%s' for path '%s' at before_version '%s'" % (page.slug, page.path, page.current_version.revision)
    page.current_version = modified_version
    page.save()
    
    page_change = PageChange.objects.create(version = modified_version, page = page, action = 'modified')
    print "created page_change '%s' for page '%s'" % (page_change.action, page_change.page.path, )
    
    file_handler = get_file_handler(page)
    page_content = open(page_path).read()
    paragraphs = file_handler.split(page_content, file_name = page_path)
    paragraphs_list = []
    matched_paragraphs = []
    for ordinal, paragraph_content in enumerate(paragraphs):
        N = paragraphs[:ordinal].count(paragraph_content)
#        print 'N %s' % (N)
        try:
            history_paragraph = Paragraph.objects.filter(page = page, current_version = before_version, original = paragraph_content)[N]
            if history_paragraph not in matched_paragraphs:       
#                print 'found history_paragraph %s' % (history_paragraph.id)
                matched_paragraphs.append(history_paragraph)
            else:
                history_paragraph = None
        except IndexError:
            history_paragraph = None
        paragraphs_list.append([paragraph_content, ordinal+ 1, history_paragraph, False])
        #(paragraph_content, ordinal+ 1, history_paragraph, 'handled?')
    print 'len(paragraphs_list) %s' % len([p for p in paragraphs_list if not p[3]])
    for i, p in enumerate(paragraphs_list):
        if p[2] and not p[3]:
            print 'updating history_paragraph %s' % (p[2].id)
            p[2].ordinal = p[1]
            p[2].current_version = modified_version
            p[2].save()
            p[3] = True
    print 'len(paragraphs_list) %s' % len([p for p in paragraphs_list if not p[3]])
    for i, p in enumerate(paragraphs_list):
        if not p[3]:
            paragraph_content_set = set(line.strip() for line in p[0].decode('utf-8').splitlines())
            for p_in_db in Paragraph.objects.filter(page = page, current_version = before_version, modified_paragraph = None):
                p_in_db_content_set = set(line.strip() for line in p_in_db.original.splitlines())
                similarity = 1.0 * len(paragraph_content_set&p_in_db_content_set) / len(paragraph_content_set)
                if similarity > min_similarity:
                    paragraph = Paragraph.objects.create(page = page, current_version = modified_version,
                                                         original = p[0], ordinal = p[1], history_paragraph = p_in_db)

                    history_translation =  p_in_db.latest_translation
                    if history_translation:
                        new_translation = Translation.objects.create(paragraph = paragraph, history_translation = history_translation,
                                                                     translator = history_translation.translator,
                                                                     content = history_translation.content,
                                                                     ip = history_translation.ip,
                                                                     )
                        
                    print 'similarity %s' % similarity
                    print 'paragraph %s(ord:%s) found history_paragraph %s(ord:%s)' % (paragraph.id, paragraph.ordinal, paragraph.history_paragraph.id, paragraph.history_paragraph.ordinal)
                    page_change.paragraphs.add(paragraph)
                    p[3] = True
                    break
    print 'len(paragraphs_list) %s' % len([p for p in paragraphs_list if not p[3]])
    for i, p in enumerate(paragraphs_list):
        if not p[3]:
            paragraph = Paragraph.objects.create(page = page, current_version = modified_version,
                                                 original = p[0], ordinal = p[1])
            page_change.paragraphs.add(paragraph)
            p[3] = True
    unhandled_length = len([p for p in paragraphs_list if not p[3]])
    print 'len(paragraphs_list) %s' % unhandled_length
    if unhandled_length != 0:
        raise ValidationError, u"paragraphs %s didn't handled " % (u",".join([str(p[1]) for p in paragraphs_list if not p[3]]), )
    
    paragraphs_count_in_db = Paragraph.objects.filter(page = page, current_version = modified_version).count()
    if len(paragraphs) != paragraphs_count_in_db:
        raise ValidationError, u"paragraphs count in file '%s' diff from count in db %s " % (len(paragraphs), paragraphs_count_in_db)
        
    page.check()
    
    print
    
@transaction.commit_manually
def handle_project(project):
    try:
        client = pysvn.Client()
        client.exception_style = 1
        doc_dir =  project.doc_path
        print doc_dir
        current_version_in_dir = client.info(doc_dir).revision
        print "current_version_in_dir is '%s'" % current_version_in_dir.number
        
        try:
            current_version_in_db = Version.objects.filter(project = project).latest('created')
            print "current_version_in_db is '%s'" % current_version_in_db.revision
            current_version_in_db_pysvn = pysvn.Revision(pysvn.opt_revision_kind.number, int(current_version_in_db.revision))
            if int(current_version_in_db.revision) == int(current_version_in_dir.number):
                print "current_version_in_db == current_version_in_dir."
                for page in Page.objects.filter(project = project, deleted = False, current_version = current_version_in_db):
                    print 'checking %s' % page.path
                    page.check()
                return
            elif int(current_version_in_db.revision) > int(current_version_in_dir.number):
                raise ValidationError, "current_version_in_db > current_version_in_dir."
            else:
                os.chdir(doc_dir)
                diff_summarize = client.diff_summarize(doc_dir, current_version_in_db_pysvn, doc_dir, current_version_in_dir)
                added_files, modified_files, deleted_files = [], [], []
                for diff in diff_summarize:
                    diff_path = diff.path.replace('\\', '/')
                    if diff.summarize_kind == pysvn.diff_summarize_kind.delete and diff.node_kind == pysvn.node_kind.dir:
                        deleted_pages = Page.objects.filter(project = project, deleted = False, current_version = current_version_in_db, path__startswith = diff_path).values_list('path', flat=True)
                        for deleted_page in  deleted_pages:
                            path = os.path.join(doc_dir, deleted_page).replace('\\', '/')
                            simple_path = deleted_page.replace('\\', '/')
                            deleted_files.append((path, simple_path))
                            
                    if diff.node_kind == pysvn.node_kind.file:
                        path = os.path.join(doc_dir, diff.path).replace('\\', '/')
                        simple_path = diff.path.replace('\\', '/')
                        if project.is_doc_file(simple_path):
                            if diff.summarize_kind == pysvn.diff_summarize_kind.added:
                                added_files.append((path, simple_path))
                            if diff.summarize_kind == pysvn.diff_summarize_kind.modified:
                                modified_files.append((path, simple_path))
                            if diff.summarize_kind == pysvn.diff_summarize_kind.delete:
                                deleted_files.append((path, simple_path))
                    #TODO 处理exclude_dir_names 变更导致的文件增删。
                handling_version_in_db = Version.objects.create(project = project, revision = current_version_in_dir.number, last_version = current_version_in_db)
                print "created handling_version_in_db '%s'." % handling_version_in_db.revision
                
                for path, simple_path in added_files:
                    handle_page_added(project, handling_version_in_db, path, simple_path)
                
                for path, simple_path in modified_files:
                    handle_page_modified(project, current_version_in_db, handling_version_in_db, path, simple_path)
                
                for path, simple_path in deleted_files:
                    handle_page_deleted(project, current_version_in_db, handling_version_in_db, path, simple_path)
                
                un_modified_pages = Page.objects.filter(project = project, deleted = False, current_version = current_version_in_db)
                for page in un_modified_pages:
                    paragraphs = page.paragraphs.filter(current_version = current_version_in_db)
                    for p in paragraphs:
                        p.current_version = handling_version_in_db
                        p.save()
                    page.current_version = handling_version_in_db
                    page.save()
                
        except Version.DoesNotExist:
            print "no current_version_in_db in db."
            handling_version_in_db = Version.objects.create(project = project, revision = current_version_in_dir.number)
            print "created current_version_in_db '%s'." % handling_version_in_db.revision
            
            files = [(path, get_simple_path(doc_dir, path).replace('\\', '/') )for path, info_dict in client.info2(doc_dir) if os.path.isfile(path)]
            
            print "%s files in doc_dir, " % len(files),
            doc_files = [(path, simple_path)for path, simple_path in files if project.is_doc_file(simple_path)]
            print "%s doc files." % len(doc_files)
            for path, simple_path in doc_files:
                handle_page_added(project, handling_version_in_db, path, simple_path)
        
        now_pages_in_db = set(Page.objects.filter(project = project, deleted = False, current_version = handling_version_in_db).values_list('path', flat=True))
        now_files_in_dir = [get_simple_path(doc_dir, path).replace('\\', '/') for path, info_dict in client.info2(doc_dir) if os.path.isfile(path)]
        now_pages_in_dir = set([path for path in now_files_in_dir if project.is_doc_file(path)])
        if now_pages_in_db != now_pages_in_dir:
            raise ValidationError, u"project pages in dir diff from pages in db\n\n%s\n\n" % ("\n".join(now_pages_in_db ^ now_pages_in_dir))
        for page in Page.objects.filter(project = project, deleted = False, current_version = handling_version_in_db):
            page.check()
            
#        raise ValidationError, u"for debug"
    
    except BaseException, args:
        import traceback
        traceback.print_exc()
#        print "get exception %s:%s" % (args.__class__.__name__, args)
        print "rollbacking database operations"
        transaction.rollback()
        print "rollbacked database operations"
    else:
        transaction.commit()
        
        
class Command(LabelCommand):
    help = "Sync project docs for the given label(s) in the database."
    
    def handle(self, *labels, **options):
        if not labels:
            labels = []

        output = []
        for label in labels:
            label_output = self.handle_label(label, **options)
            if label_output:
                output.append(label_output)
        return '\n'.join(output)
    
    def handle_label(self, label, **options):
        try:
            project = Project.objects.get(slug = label)
            print "found project '%s' in database." % label
            handle_project(project)
            print "synced docs for project '%s'.\n" % label
        except Project.DoesNotExist:
            print "project '%s' didn't exist in database." % label
            return