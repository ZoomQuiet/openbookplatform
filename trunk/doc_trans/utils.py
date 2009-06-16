# -*- coding: utf-8 -*-
from django.utils.importlib import import_module
import os,zipfile

def get_file_handler(page):
    try:
        project_module_name = u"doc_trans.file_handlers.projects.%s.%s" % (page.project.slug.replace('-', '_'), page.doc_type)
#        print "try file_handlers at '%s'" % (project_module_name, )
        file_handler = import_module(project_module_name)
    except ImportError:
        page_doc_type_module_name = u"doc_trans.file_handlers.%s" % page.doc_type
#        print "try file_handlers at '%s'" % (page_doc_type_module_name, )
        file_handler = import_module(page_doc_type_module_name)
    return file_handler

def get_update_handlers(project):
    try:
        project_module_name = u"doc_trans.update_handlers.projects.%s_handler" % (project.slug.replace('-', '_'))
        print "try update_handlers at '%s'" % (project_module_name, )
        update_handler = import_module(project_module_name)
    except ImportError:
        repository_type_module_name = u"doc_trans.update_handlers.%s" % project.repository_type
        print "try update_handlers at '%s'" % (repository_type_module_name, )
        update_handler = import_module(repository_type_module_name)
    return update_handler

def get_export_handler(project):
    try:
        project_module_name = u"doc_trans.export_handler.projects.%s_handler" % (project.slug.replace('-', '_'))
        print "try export_handler at '%s'" % (project_module_name, )
        handler = import_module(project_module_name)
    except ImportError:
        svn_module_name = u"doc_trans.export_handlers.%s" % 'svn'
        print "try export_handlers at '%s'" % (svn_module_name, )
        handler = import_module(svn_module_name)
    return handler

def get_exported_after_handler(project):
    try:
        project_module_name = u"doc_trans.export_handlers.after_handlers.projects.%s_handler" % (project.slug.replace('-', '_'))
        print "try after_handlers at '%s'" % (project_module_name, )
        handler = import_module(project_module_name)
    except ImportError:
        project_doc_type_module_name = u"doc_trans.export_handlers.after_handlers.%s_handler" % project.doc_type
        print "try after_handlers at '%s'" % (project_doc_type_module_name, )
        handler = import_module(project_doc_type_module_name)
    return handler

def get_url_handler(project):
    try:
        project_module_name = u"doc_trans.url_handlers.projects.%s_urls" % (project.slug.replace('-', '_'))
        print "try url_handlers at '%s'" % (project_module_name, )
        handler = import_module(project_module_name)
    except ImportError:
        static_module_name = u"doc_trans.url_handlers.%s" % 'static'
        print "try url_handlers at '%s'" % (static_module_name, )
        handler = import_module(static_module_name)
    return handler

def zipfolder(foldername, filename):
    if os.path.exists(filename):
        os.remove(filename)
    zip = zipfile.ZipFile(filename, "w",)
    foldername = foldername.replace('\\', '/')
    print 'compressing %s to %s' % (foldername, filename)
    for root, dirs, files in os.walk(foldername):
        for name in dirs:
            if name.startswith('.'):
                dirs.remove(name)
        for name in files:
            full_path = os.path.join(root, name).replace('\\', '/').encode('utf-8')
            arcname = full_path.replace(foldername + '/', '').encode('utf-8')
            zip.write(full_path, arcname)
            

def get_simple_path(base_dir, full_path):
    base_dir = os.path.normpath(base_dir)
    full_path = os.path.normpath(full_path)
    simple_path = full_path.replace(base_dir + os.sep, '')
    return simple_path