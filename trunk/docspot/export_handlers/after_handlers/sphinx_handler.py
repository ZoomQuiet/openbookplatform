# -*- coding: utf-8 -*-
from django.conf import settings
import os
import shutil
from doc_trans.utils import zipfolder


def build_docs(srcdir, destdir, confdir = None, page = None):
    current_dir = os.getcwd()
    os.chdir(srcdir)

    _build_destdir = destdir
    args = ['sphinx-build',                          # Fake argv[0]
            '-b', 'html',                            # Use the JSON builder
            '-q',                                    # Do not output anything on standard output, only write warnings and errors to standard error. 
            srcdir,                                  # Source file directory
            _build_destdir,                          # Destination directory
            ]
    
    if confdir:
        args.insert(1, confdir)
        args.insert(1, '-c')
    
    if page:
        args.append(os.path.join(srcdir, page.path))
    else:
        if os.path.exists(destdir):
            shutil.rmtree(destdir)
        if not os.path.exists(_build_destdir):
            os.makedirs(_build_destdir)
            
    import sphinx
    sphinx.main(args)
    os.chdir(current_dir)
    
def handle_exported(project, language = None, page = None):
    web_docs_repository_path = os.path.join(settings.WEB_DOCS_DIR, project.slug, )
    doc_dir =  os.path.join(web_docs_repository_path, settings.ORIGINAL_LANGUAGE)
    exprot_dir = os.path.join(web_docs_repository_path, settings.TRANSLATION_LANGUAGE)
    
    if page:
        build_docs(project.export_path, exprot_dir, page = page)
        return
    
    if language == None:
        build_docs(project.doc_path, doc_dir)
        build_docs(project.export_path, exprot_dir)
    elif language == settings.ORIGINAL_LANGUAGE:
        build_docs(project.doc_path, doc_dir)
    elif language == settings.TRANSLATION_LANGUAGE:
        build_docs(project.export_path, exprot_dir)
#    zipfolder(os.path.join(web_docs_repository_path, settings.ORIGINAL_LANGUAGE), os.path.join(web_docs_repository_path, settings.ORIGINAL_LANGUAGE + '.zip'))
#    zipfolder(os.path.join(web_docs_repository_path, settings.TRANSLATION_LANGUAGE), os.path.join(web_docs_repository_path, settings.TRANSLATION_LANGUAGE + '.zip'))

