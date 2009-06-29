# -*- coding: utf-8 -*-
from django.conf import settings
docs_dir = settings.DOCS_DIR
import os
import pysvn
from doc_trans.update_handlers import svn
from doc_trans.update_handlers.projects import download_project

def update(project, revision):
    svn.update(project, revision)
    svn_url = 'http://svn.sqlalchemy.org/sqlalchemy/trunk/lib/sqlalchemy/'
    to_dir_name = 'sqlalchemy-trunk'
    recurse = False
    download_project.download(project, revision, svn_url, to_dir_name, recurse = recurse)