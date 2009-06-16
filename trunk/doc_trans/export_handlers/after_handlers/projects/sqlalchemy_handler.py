# -*- coding: utf-8 -*-
from django.conf import settings
import os
import shutil
import re
import pysvn
from doc_trans.export_handlers.after_handlers.sphinx_handler import build_docs
from doc_trans.export_handlers.after_handlers.projects.setup_sphinx_dev import Setuper

            
def handle_problem_file_name(problem_file_name, version_info_file):
    print problem_file_name
    file_content = open(problem_file_name).read()
    file_content = re.sub(r'import sqlalchemy', '', file_content)
    version_info_file_content = open(version_info_file).read()
    version_info = re.search(r"__version__ = '(.+?)'", version_info_file_content).group(1)
    file_content = re.sub(r'sqlalchemy\.__version__', '"%s"' % version_info, file_content)
    problem_file = open(problem_file_name, 'w')
    problem_file.write(file_content)
    problem_file.close()
    
def handle_exported(project, language = None, page = None):
    web_docs_repository_path = os.path.join(settings.WEB_DOCS_DIR, project.slug, )
    doc_dir =  os.path.join(web_docs_repository_path, settings.ORIGINAL_LANGUAGE)
    exprot_dir = os.path.join(web_docs_repository_path, settings.TRANSLATION_LANGUAGE)
    
    version_info_file = os.path.join(project.root, 'sqlalchemy-trunk', '__init__.py')
    if not page:
        temp_project_doc_path = project.doc_path + '-temp'
        client = pysvn.Client()
        client.exception_style = 1
        if os.path.exists(temp_project_doc_path):
            shutil.rmtree(temp_project_doc_path)
        client.export(project.doc_path, temp_project_doc_path)
        problem_file_name = os.path.join(temp_project_doc_path, 'conf.py')
        handle_problem_file_name(problem_file_name, version_info_file)
        
    problem_file_name = os.path.join(project.export_path, 'conf.py')
    handle_problem_file_name(problem_file_name, version_info_file)
    
    setuper = Setuper()
    setuper.setup()
    
    if page:
        build_docs(project.export_path, exprot_dir, page = page)
        return
    
    if language == None:
        build_docs(temp_project_doc_path, doc_dir)
        build_docs(project.export_path, exprot_dir)
    elif language == settings.ORIGINAL_LANGUAGE:
        build_docs(temp_project_doc_path, doc_dir)
    elif language == settings.TRANSLATION_LANGUAGE:
        build_docs(project.export_path, exprot_dir)
        
    
    setuper.restore()
    