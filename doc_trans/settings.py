# -*- coding: utf-8 -*-

REPOSITORY_TYPES = (('svn', 'Subversion'),
                   ('hg', 'Mercurial'),
                   ('cvs', 'Concurrent Versions System'),
                   ('local', 'Local Directory'),
                   )

DOC_TYPES = (('sphinx', 'Sphinx'),
             ('docutils', 'Docutils'),
             ('html', 'HTML'),
             ('textile', 'Textile'),
             )

LEXER_NAME_MAP = {'sphinx':'rst',
                  'docutils':'rst',
                  'html':'html',
                  'textile':'textile',
                  }

PAGE_CHANGE_ACTION_TYPES = (('added', 'Added'),
                            ('modified', 'Modified'),
                            ('deleted', 'Deleted'),
                            )