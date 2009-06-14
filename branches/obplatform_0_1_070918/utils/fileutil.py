import os, sys
from django.conf import settings

def getfilename(filename, subdir=''):
    if subdir:
        return os.path.join(settings.MEDIA_ROOT, subdir, filename)
    else:
        return os.path.join(settings.MEDIA_ROOT, filename)
    
def resetfilename(filename, subdir=''):
    fname = getfilename(filename, subdir)
    if os.path.exists(fname):
        try:
            os.remove(fname)
        except:
            pass
    dirs = os.path.dirname(fname)
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    return fname

def encodefilename(filename):
    return unicode(filename, settings.DEFAULT_CHARSET).encode(sys.getfilesystemencoding())
        