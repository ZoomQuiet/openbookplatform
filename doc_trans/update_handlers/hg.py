# -*- coding: utf-8 -*-
from django.conf import settings
docs_dir = settings.DOCS_DIR
import os
import pysvn
from doc_trans.update_handlers.svn_helpers import *
from doc_trans.update_handlers.hg_helpers import *

def update(project, revision):
    doc_dir =  os.path.join(docs_dir, project.slug, settings.HG_REPO_NAME)

    print 'repo %s' % (project.repository_url,)
    exists = os.path.exists(doc_dir)

    client = pysvn.Client()
    client.exception_style = 1
    svn_doc_dir = os.path.join(doc_dir, project.doc_dir_name)
    svn_doc_url = settings.LOCAL_SVN_URL + project.slug
    svn_check_in_dir = project.doc_path
    original_doc_dir = svn_doc_dir

    if exists:
        os.chdir(doc_dir)
        hg_pull(project.repository_url, revision, update = True, verbose = True)
        
        remove_first(client, svn_check_in_dir, original_doc_dir, project)
        
        copy_and_checkin(client, svn_check_in_dir, original_doc_dir, svn_doc_url, project)
        
    else:
        project_dir = os.path.join(docs_dir, project.slug)
        if not os.path.exists(project_dir): os.makedirs(project_dir)
        os.chdir(project_dir)
        hg_clone(project.repository_url, settings.HG_REPO_NAME, revision, True)
        
        import_to_repo(client, svn_check_in_dir, svn_doc_dir, svn_doc_url, project)
        
        os.chdir(os.path.join(settings.DOCS_DIR, project.slug))
        checkout_after_import(client, svn_doc_url, settings.ORIGINAL_LANGUAGE)
    
    check_sync(svn_check_in_dir, original_doc_dir)
    
    print 'current py_revision %s' % (client.info(svn_check_in_dir).revision)
        
    print '\n'
    os.chdir(doc_dir)
    hg_tip()