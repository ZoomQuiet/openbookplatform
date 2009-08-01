# -*- coding: utf-8 -*-
import os
import pysvn

def download(project, revision, svn_url, to_dir_name, recurse = True):
    client = pysvn.Client()
    client.exception_style = 1
    to_dir = os.path.join(project.root, to_dir_name)
    exists = os.path.exists(to_dir)
    py_revision = pysvn.Revision(pysvn.opt_revision_kind.number, int(revision)) if revision else pysvn.Revision(pysvn.opt_revision_kind.head)
    if exists:
        os.chdir(to_dir)
        client.update(to_dir, revision = py_revision, recurse = recurse)
    else:
        os.chdir(project.root)
        client.checkout(svn_url, to_dir_name, revision = py_revision, recurse = recurse)
    