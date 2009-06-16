# -*- coding: utf-8 -*-
import os
import sys
from optparse import make_option

from django.core.management.base import LabelCommand, CommandError
from django.utils.importlib import import_module
from doc_trans.models import Project
from doc_trans.utils import get_update_handlers

class Command(LabelCommand):
    option_list = LabelCommand.option_list + (
        make_option('-r', '--revision', dest='revision', default=None,
                        help='The version you want to update to.'),
        )
    help = "Update project docs for the given label(s) in the docs directory."
    
    def handle(self, *labels, **options):
        if len(labels) != 1 and options['revision'] != None:
            raise CommandError(u'Only use --revision when enter 1 label.')
        
        if not labels:
            labels = []

        output = []
        for label in labels:
            label_output = self.handle_label(label, **options)
            if label_output:
                output.append(label_output)
        return '\n'.join(output)
    
    def handle_label(self, label, **options):
        revision = options['revision']
        try:
            project = Project.objects.get(slug = label)
            print "found project '%s' in database." % label
            
            update_handler = get_update_handlers(project)
            update_handler.update(project, revision)
            
            print "updated docs for project '%s'.\n" % label
        except Project.DoesNotExist:
            print "project '%s' didn't exist in database." % label
            return