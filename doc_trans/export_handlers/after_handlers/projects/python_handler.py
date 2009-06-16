# -*- coding: utf-8 -*-
from doc_trans.export_handlers.after_handlers.projects.setup_sphinx_dev import Setuper
from doc_trans.export_handlers.after_handlers import sphinx_handler       

def handle_exported(project, language = None, page = None):
    setuper = Setuper()
    setuper.setup()
    sphinx_handler.handle_exported(project, language = language, page = page)
    setuper.restore()
