# -*- coding: utf-8 -*-
from django.conf import settings
import os
import pysvn
from doc_trans.models import Version
from doc_trans.utils import get_file_handler
import shutil

def export(project, language = None):
    doc_dir =  project.doc_path
    client = pysvn.Client()
    client.exception_style = 1
    exists = os.path.exists(doc_dir)
    try:
        if exists:
            os.chdir(doc_dir)
            current_version_in_dir = client.info(doc_dir).revision
            print "current_version_in_dir is '%s'" % current_version_in_dir.number
            current_version_in_db = Version.objects.filter(project = project).latest('created')
            print "current_version_in_db is '%s'" % current_version_in_db.revision
            if int(current_version_in_db.revision) == int(current_version_in_dir.number):
                print "current_version_in_db == current_version_in_dir."
                exprot_dir = os.path.join(settings.DOCS_DIR, project.slug, settings.TRANSLATION_LANGUAGE)
                if os.path.exists(exprot_dir):
                    shutil.rmtree(exprot_dir)
                print 'export_dir: %s ' % exprot_dir
                client.export(doc_dir, exprot_dir)
                print 'exported'
                for page in project.current_pages:
                    page.write_page()
                    print "wrote page %s" % page.path
                    
            else:
                print "current_version_in_db != current_version_in_dir."
        else:
            print u"the doc dir '%s' not exist" % (doc_dir)
        
    except pysvn.ClientError, e:
        for message, code in e.args[1]:
            print 'Code:',code,'Message:',message