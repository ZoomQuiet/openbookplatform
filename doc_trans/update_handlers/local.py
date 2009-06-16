# -*- coding: utf-8 -*-
from django.conf import settings
import os
import pysvn
from django.core.exceptions import ValidationError
from doc_trans.update_handlers.svn_helpers import *

def update(project, revision):
    svn_doc_url = settings.LOCAL_SVN_URL + project.slug
    svn_check_in_dir = project.doc_path
    original_doc_dir =  os.path.join(settings.DOCS_DIR, project.slug, project.repository_url)
    doc_dir = project.doc_path
    client = pysvn.Client()
    client.exception_style = 1
    exists = os.path.exists(doc_dir)
    try:
        print svn_doc_url
        print svn_check_in_dir
        print original_doc_dir
        if exists:
            remove_first(client, svn_check_in_dir, original_doc_dir, project)
            
            copy_and_checkin(client, svn_check_in_dir, original_doc_dir, svn_doc_url, project)
            
        else:
            print 'import_to_repo %s' % (svn_doc_url)
            import_to_repo(client, svn_check_in_dir, original_doc_dir, svn_doc_url, project)
            
            os.chdir(os.path.join(settings.DOCS_DIR, project.slug))
            checkout_after_import(client, svn_doc_url, settings.ORIGINAL_LANGUAGE)
        
        check_sync(svn_check_in_dir, original_doc_dir)
        print 'current py_revision %s' % (client.info(doc_dir).revision)
    except pysvn.ClientError, e:
        for message, code in e.args[1]:
            print 'Code:',code,'Message:',message