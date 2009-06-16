# -*- coding: utf-8 -*-
from django.conf import settings
import os
import sys
import shutil
import pysvn
from doc_trans.utils import zipfolder

def generate_guides(full_dir, doc_dir):
    os.chdir(os.path.join(full_dir, 'railties',))
    output = os.path.join(full_dir, 'railties', 'guides', 'output')
    if os.path.exists(output):
        shutil.rmtree(output)
        
    cmd = 'rake generate_guides'
    print cmd
    os.system(cmd)
    
    if os.path.exists(doc_dir):
        shutil.rmtree(doc_dir)
        
    shutil.copytree(output, doc_dir)
    
def handle_exported(project, language = None, page = None):
    full_dir = os.path.join(settings.DOCS_DIR, project.slug, 'rails')
    guides_dir = os.path.join(full_dir, 'railties', 'guides')
    if os.path.exists(guides_dir):
        shutil.rmtree(guides_dir)
    client = pysvn.Client()
    client.exception_style = 1
    client.export(project.doc_path, guides_dir)
    
    web_docs_repository_path = os.path.join(settings.WEB_DOCS_DIR, project.slug, )
    doc_dir =  os.path.join(web_docs_repository_path, settings.ORIGINAL_LANGUAGE)
    generate_guides(full_dir, doc_dir)
    
    shutil.rmtree(guides_dir)
    cn_exprot_dir = os.path.join(settings.DOCS_DIR, project.slug, settings.TRANSLATION_LANGUAGE)
    shutil.copytree(cn_exprot_dir, guides_dir)
    exprot_dir = os.path.join(web_docs_repository_path, settings.TRANSLATION_LANGUAGE)
    generate_guides(full_dir, exprot_dir)