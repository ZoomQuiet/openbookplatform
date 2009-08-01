# -*- coding: utf-8 -*-

from django.conf import settings
import os
import sys
lib_dir = os.path.abspath(os.path.join(settings.DOCS_DIR, 'sphinx', settings.HG_REPO_NAME))

class Setuper(object):
    
    def setup(self):
        self.path = []
        for k in [k for k in sys.modules if k.startswith('sphinx')]:
            del sys.modules[k]
        for i,k in enumerate(sys.path):
            if k.find('Sphinx') != -1:
                self.path.append((i, sys.path.pop(i)))
        sys.path.insert(0, lib_dir)
        
    def restore(self):
        for k in [k for k in sys.modules if k.startswith('sphinx')]:
            del sys.modules[k]
        sys.path.remove(lib_dir)
        for i,path in self.path:
            sys.path.insert(i, path)
    
