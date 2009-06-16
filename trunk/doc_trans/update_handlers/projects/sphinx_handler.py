# -*- coding: utf-8 -*-
from django.conf import settings
docs_dir = settings.DOCS_DIR
import os
import shutil

from doc_trans.update_handlers import hg

def update(project, revision):
    hg.update(project, revision)
    CHANGES = os.path.join(docs_dir, project.slug, settings.HG_REPO_NAME, 'CHANGES')
    EXAMPLES = os.path.join(docs_dir, project.slug, settings.HG_REPO_NAME, 'EXAMPLES')
    shutil.copyfile(CHANGES, os.path.join(docs_dir, project.slug, 'CHANGES'))
    shutil.copyfile(EXAMPLES, os.path.join(docs_dir, project.slug, 'EXAMPLES'))
    
    