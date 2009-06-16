# -*- coding: utf-8 -*-
import os
from django.core.exceptions import ValidationError
import shutil
from doc_trans.utils import get_simple_path
from django.conf import settings
import datetime

def dump_repos(filename = u'dump_repos'):
    SVN_DOCS_BACKUP_DIR = settings.SVN_DOCS_BACKUP_DIR
    if not os.path.exists(SVN_DOCS_BACKUP_DIR):
        os.makedirs(SVN_DOCS_BACKUP_DIR)
    filename = u"%s.%s" % (datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), filename)
    cmd = 'svnadmin dump %s > %s' % (settings.SVN_DOCS_DIR, os.path.join(SVN_DOCS_BACKUP_DIR, filename))
    print cmd
    os.system(cmd)
    
def copy_files(original_doc_dir, svn_check_in_dir):
    for root, dirs, files in os.walk(original_doc_dir):
        for name in files:
            full_path = os.path.join(root, name)
            simple_path = get_simple_path(original_doc_dir, full_path)
            svn_doc_path = os.path.join(svn_check_in_dir, simple_path)
            if not os.path.exists(os.path.dirname(svn_doc_path)):
                os.makedirs(os.path.dirname(svn_doc_path))
            shutil.copy2(full_path, svn_doc_path)
            
            
def remove_first(client, svn_check_in_dir, original_doc_dir, project):
    old_py_revision = client.info(svn_check_in_dir).revision
    dump_repos(filename = u'r%s.%s_remove_first' % (old_py_revision.number, project.slug))
    
    for root, dirs, files in os.walk(svn_check_in_dir):
#        print 'root %s' % root
#        print 'dirs %s' % dirs
#        print 'files %s' % files
        if '.svn' in dirs:
            dirs.remove('.svn')
        for name in files:
            full_path = os.path.join(root, name)
            simple_path = get_simple_path(svn_check_in_dir, full_path)
            original_doc_path = os.path.join(original_doc_dir, simple_path)
            if not os.path.exists(original_doc_path):
                print '%s remove_first' % simple_path 
                client.remove(full_path, force=True)
        for name in dirs:
            full_path = os.path.join(root, name)
            simple_path = get_simple_path(svn_check_in_dir, full_path)
            original_doc_path = os.path.join(original_doc_dir, simple_path)
            if not os.path.exists(original_doc_path):
                print '%s remove_first' % simple_path 
                client.remove(full_path, force=True)
    client.checkin(svn_check_in_dir, log_message = 'checkin for delete')
    client.update(svn_check_in_dir)

def copy_and_checkin(client, svn_check_in_dir, original_doc_dir, svn_doc_url, project):
    old_py_revision = client.info(svn_check_in_dir).revision
    dump_repos(filename = u'r%s.%s_copy_and_checkin' % (old_py_revision.number, project.slug))
    
    print 'old py_revision %s' % (old_py_revision, )
    
    print "checkin svn repo for doc dir '%s' at '%s'" % (svn_check_in_dir, svn_doc_url)
#    os.system('cp -a %s/* %s' % (original_doc_dir, svn_check_in_dir))
    copy_files(original_doc_dir, svn_check_in_dir)
    
    
    
    os.chdir(svn_check_in_dir)
    client.add('.', force = True)
    client.checkin(svn_check_in_dir, log_message = 'checkin')
#    print "checkin svn repo for doc dir '%s' at '%s'" % (svn_check_in_dir, svn_doc_url)
    
    print "update svn repo for doc dir '%s' at '%s'" % (svn_check_in_dir, svn_doc_url)
    client.update(svn_check_in_dir)
#    print "updated svn repo for doc dir '%s' at '%s'" % (svn_check_in_dir, svn_doc_url)
    
    print 'diff_summarize:\n'
    for diff in client.diff_summarize(svn_check_in_dir, old_py_revision, svn_check_in_dir, client.info(svn_check_in_dir).revision):
        print diff.path, diff.summarize_kind
                
                
def check_sync(svn_check_in_dir, original_doc_dir):
    for root, dirs, files in os.walk(original_doc_dir):
        for name in files:
            full_path = os.path.join(root, name)
            simple_path = get_simple_path(original_doc_dir, full_path)
            svn_doc_path = os.path.join(svn_check_in_dir, simple_path)
            if not os.path.exists(svn_doc_path):
                raise ValidationError, "'%s' didn't exist in svn_doc_path" % svn_doc_path
        for name in dirs:
            full_path = os.path.join(root, name)
            simple_path = get_simple_path(original_doc_dir, full_path)
            svn_doc_path = os.path.join(svn_check_in_dir, simple_path)
            if not os.path.exists(svn_doc_path):
                raise ValidationError, "'%s' didn't exist in svn_doc_path" % svn_doc_path
    
    for root, dirs, files in os.walk(svn_check_in_dir):
        if '.svn' in dirs:
            dirs.remove('.svn')
        for name in files:
            full_path = os.path.join(root, name)
            simple_path = get_simple_path(svn_check_in_dir, full_path)
            original_doc_path = os.path.join(original_doc_dir, simple_path)
            if not os.path.exists(original_doc_path):
                raise ValidationError, "'%s' didn't exist in original_doc_path" % original_doc_path
        for name in dirs:
            full_path = os.path.join(root, name)
            simple_path = get_simple_path(svn_check_in_dir, full_path)
            original_doc_path = os.path.join(original_doc_dir, simple_path)
            if not os.path.exists(original_doc_path):
                raise ValidationError, "'%s' didn't exist in original_doc_path" % original_doc_path
            
def import_to_repo(client, svn_check_in_dir, original_doc_dir, svn_doc_url, project):
    old_py_revision = client.info2(settings.LOCAL_SVN_URL, recurse=False)[0][1]['rev']
    
    dump_repos(filename = u'r%s.%s_import_to_repo' % (old_py_revision.number, project.slug))
    
    
    print "creating svn repo for doc dir '%s' at '%s'" % (original_doc_dir, svn_doc_url)
    
    client.import_(original_doc_dir, svn_doc_url, log_message = 'Initial import')
#    print "creatd svn repo for doc dir '%s' at '%s'" % (original_doc_dir, svn_doc_url)

def checkout_after_import(client, svn_doc_url, checkout_to):
    print "checkout svn repo for doc dir '%s' at '%s'" % (checkout_to, svn_doc_url)
    client.checkout(svn_doc_url, checkout_to)