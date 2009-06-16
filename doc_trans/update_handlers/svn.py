# -*- coding: utf-8 -*-
from django.conf import settings
docs_dir = settings.DOCS_DIR
import os
import pysvn

def update(project, revision):
    doc_dir =  project.doc_path
    client = pysvn.Client()
    client.exception_style = 1
#    print client.info(doc_dir).revision
#    os.chdir(doc_dir)
#    print os.getcwd()
#    client.update(project.repository_url, depth = pysvn.depth.infinity )
    exists = os.path.exists(doc_dir)
    py_revision = pysvn.Revision(pysvn.opt_revision_kind.number, int(revision)) if revision else pysvn.Revision(pysvn.opt_revision_kind.head)
    try:
        if exists:
            os.chdir(doc_dir)
            old_py_revision = client.info(doc_dir).revision
            print 'update from %s to py_revision %s at %s' % (old_py_revision, py_revision, doc_dir)
            client.update(doc_dir, revision = py_revision)
            print 'diff_summarize:\n'
#            for diff in client.diff_summarize(doc_dir, old_py_revision, doc_dir, py_revision):
#                print diff.path, diff.summarize_kind
#                for k,v in diff.items():
#                    print k,v
        else:
            project_dir = os.path.join(docs_dir, project.slug)
            if not os.path.exists(project_dir): os.makedirs(project_dir)
            os.chdir(project_dir)
            print 'get py_revision %s to %s' % (py_revision, project_dir)
            client.checkout(project.repository_url, settings.ORIGINAL_LANGUAGE, revision = py_revision)
        print 'current py_revision %s' % (client.info(doc_dir).revision)
    except pysvn.ClientError, e:
        for message, code in e.args[1]:
            print 'Code:',code,'Message:',message