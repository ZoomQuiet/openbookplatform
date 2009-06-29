# -*- coding: utf-8 -*-
from django.conf import settings
import os
import shutil
from doc_trans.utils import zipfolder, get_simple_path

def copy_files(original, dest, page = None):
    if page:
        original_path = os.path.join(original, page.path)
        dest_path = os.path.join(dest, page.path)
        print original_path
        print dest_path
        shutil.copy2(original_path, dest_path)
    else:
        if os.path.exists(dest):
            shutil.rmtree(dest)
        for root, dirs, files in os.walk(original):
            if '.svn' in dirs:
                dirs.remove('.svn')
            for name in files:
                original_path = os.path.join(root, name)
                simple_path = get_simple_path(original, original_path)
                dest_path = os.path.join(dest, simple_path)
                if not os.path.exists(os.path.dirname(dest_path)):
                    os.makedirs(os.path.dirname(dest_path))
                shutil.copy2(original_path, dest_path)
            
def handle_exported(project, language = None, page = None):
    web_docs_repository_path = os.path.join(settings.WEB_DOCS_DIR, project.slug, )
    
    if page:
        copy_files(project.export_path, os.path.join(web_docs_repository_path, settings.TRANSLATION_LANGUAGE), page = page)
        return
    
    if language == None:
        copy_files(project.doc_path, os.path.join(web_docs_repository_path, settings.ORIGINAL_LANGUAGE))
        copy_files(project.export_path, os.path.join(web_docs_repository_path, settings.TRANSLATION_LANGUAGE))
    elif language == settings.ORIGINAL_LANGUAGE:
        copy_files(project.doc_path, os.path.join(web_docs_repository_path, settings.ORIGINAL_LANGUAGE))
    elif language == settings.TRANSLATION_LANGUAGE:
        copy_files(project.export_path, os.path.join(web_docs_repository_path, settings.TRANSLATION_LANGUAGE))
        
    
    
#    zipfolder(os.path.join(web_docs_repository_path, settings.ORIGINAL_LANGUAGE), os.path.join(web_docs_repository_path, settings.ORIGINAL_LANGUAGE + '.zip'))
#    zipfolder(os.path.join(web_docs_repository_path, settings.TRANSLATION_LANGUAGE), os.path.join(web_docs_repository_path, settings.TRANSLATION_LANGUAGE + '.zip'))
    