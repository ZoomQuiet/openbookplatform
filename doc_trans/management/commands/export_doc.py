# -*- coding: utf-8 -*-
import os
import sys
from optparse import make_option

from django.core.management.base import LabelCommand, CommandError
from django.utils.importlib import import_module
from django.conf import settings
from doc_trans.models import Project
from doc_trans.utils import get_export_handler, get_exported_after_handler

class Command(LabelCommand):
    option_list = LabelCommand.option_list + (
        make_option('-l', '--language', dest='language', default=None,
                        help='The language for docs you want to export.'),
        )
    help = "Export project docs for the given label(s) in the docs directory."
    
    def handle(self, *labels, **options):
        if not labels:
            labels = []

        output = []
        for label in labels:
            label_output = self.handle_label(label, **options)
            if label_output:
                output.append(label_output)
        return '\n'.join(output)
    
    def handle_label(self, label, **options):
        language = options['language']
        if language == 'o':
            language = settings.ORIGINAL_LANGUAGE
        elif language == 't':
            language = settings.TRANSLATION_LANGUAGE
        else:
            language = None
        
        try:
            project = Project.objects.get(slug = label)
            print "found project '%s' in database." % label
            print "export project '%s' in language %s." % (project, language, )
            
            export_handler = get_export_handler(project)
            export_handler.export(project, language)
            print "export_handled for project '%s'.\n" % label
            
            exported_after_handler = get_exported_after_handler(project)
            exported_after_handler.handle_exported(project, language)
            print "exported_after_handled for project '%s'.\n" % label
            
            print "exported docs for project '%s'.\n" % label
        except Project.DoesNotExist:
            print "project '%s' didn't exist in database." % label
            return