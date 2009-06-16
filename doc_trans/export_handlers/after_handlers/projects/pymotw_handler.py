# -*- coding: utf-8 -*-
from django.conf import settings
import os
import shutil
import re
import pysvn
from doc_trans.export_handlers.after_handlers.sphinx_handler import build_docs

            
def handle_trace_index_rst(problem_file_name):
    file_content = open(problem_file_name).read()
    file_content = re.sub(r'coverdir\d/', '', file_content)
    file_content = re.sub(r'trace_example\.recurse\.cover', 'trace_example/recurse.cover', file_content)
    problem_file = open(problem_file_name, 'w')
    problem_file.write(file_content)
    problem_file.close()
    
def handle_exported(project, language = None, page = None):
    web_docs_repository_path = os.path.join(settings.WEB_DOCS_DIR, project.slug, )
    doc_dir =  os.path.join(web_docs_repository_path, settings.ORIGINAL_LANGUAGE)
    exprot_dir = os.path.join(web_docs_repository_path, settings.TRANSLATION_LANGUAGE)
    confdir = os.path.join(settings.DOCS_DIR, project.slug, settings.HG_REPO_NAME, 'sphinx')
    
    #hack
    os.environ['VERSION'] = '1.91'
    os.environ['TEMPLATES'] = 'pkg'
    
    if not page:
        temp_project_doc_path = project.doc_path + '-temp'
        client = pysvn.Client()
        client.exception_style = 1
        if os.path.exists(temp_project_doc_path):
            shutil.rmtree(temp_project_doc_path)
        client.export(project.doc_path, temp_project_doc_path)
        problem_file_name = os.path.join(temp_project_doc_path, 'trace','index.rst')
        handle_trace_index_rst(problem_file_name)
    
    problem_file_name = os.path.join(project.export_path, 'trace','index.rst')
    handle_trace_index_rst(problem_file_name)
    
    if page:
        build_docs(project.export_path, exprot_dir, confdir, page = page)
        return
    
    
    if language == None:
        build_docs(temp_project_doc_path, doc_dir, confdir)
        build_docs(project.export_path, exprot_dir, confdir)
    elif language == settings.ORIGINAL_LANGUAGE:
        build_docs(temp_project_doc_path, doc_dir, confdir)
    elif language == settings.TRANSLATION_LANGUAGE:
        build_docs(project.export_path, exprot_dir, confdir)
        