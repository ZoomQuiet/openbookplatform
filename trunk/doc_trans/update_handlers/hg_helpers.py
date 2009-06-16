# -*- coding: utf-8 -*-
import os
from django.core.exceptions import ValidationError
try:
    from mercurial import commands
    from mercurial import ui, hg
    from mercurial.util import Abort
    has_mercurial = True
except ImportError:
    has_mercurial = False
    
def hg_clone(repository_url, destdir, revision, verbose):
    print 'clone repo revision %s to %s' % (revision, destdir,)
    if has_mercurial:
        u = ui.ui()
        repo = hg.repository(u, repository_url)
        rev = [revision,] if revision else None
        commands.clone(u, repo, destdir, rev = rev, verbose = verbose)
    else:
        if revision:
            cmd = 'hg clone -r%s %s %s' % (revision, repository_url, destdir)
        else:
            cmd = 'hg clone %s %s' % (repository_url, destdir)
        print cmd
        os.system(cmd)
    print 'cloned repo to %s' % (destdir,)
        
def hg_pull(source, revision, update, verbose):
    print 'update repo revision %s at %s' % (revision, source,)
    if has_mercurial:
        u = ui.ui()
        repo = hg.repository(u, '.')
        rev = [revision,] if revision else None
        commands.pull(u, repo, source = source, rev = rev, update = update, verbose = verbose)
    else:
        if revision:
            cmd = 'hg pull -u -r%s %s' % (revision, source)
        else:
            cmd = 'hg pull -u %s' % (source)
        print cmd
        os.system(cmd)
    print 'updated repo at %s' % (source,)

def hg_tip():
    if has_mercurial:
        u = ui.ui()
        repo = hg.repository(u, '.')
        commands.tip(u, repo)
    else:
        cmd = 'hg tip'
        print cmd
        os.system(cmd)