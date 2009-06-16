# -*- coding: utf-8 -*-
from django.conf import settings
docs_dir = settings.DOCS_DIR
import os
import pysvn
from doc_trans.update_handlers import svn
from doc_trans.update_handlers.projects import download_project

def update(project, revision):
    svn.update(project, revision)
    download_project.download(project, revision, 'http://svn.turbogears.org/trunk/', 'turbogears-trunk')