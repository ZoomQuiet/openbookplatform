# -*- coding: utf-8 -*-
import re
from django.template import Template, Context
from django.core.exceptions import ValidationError

body_content_re = re.compile(r'(<body.+?</body>)', flags = re.DOTALL|re.IGNORECASE)
line_re = re.compile(r'(<div\sclass="line"></div>)', flags = re.DOTALL)
gc_pagecontent_re = re.compile(r'(<div\sclass="g-unit"\sid="gc-pagecontent">.+?<!--\send\sgc-pagecontent\s-->)', flags = re.DOTALL)
h2_re = re.compile(r'(<h2.*?>.+?</h2>)', flags = re.DOTALL|re.IGNORECASE)

def split(content, file_name = ''):
    paragraphs_content = body_content_re.split(content)
    if len(paragraphs_content) == 3:
        paragraphs = [paragraphs_content[0],]
        gc_pagecontent_paragraphs = gc_pagecontent_re.split(paragraphs_content[1])
        if len(gc_pagecontent_paragraphs) == 3:
            paragraphs.append(gc_pagecontent_paragraphs[0])
            for i, p in enumerate(h2_re.split(gc_pagecontent_paragraphs[1])):
                if i == 0:
                    paragraphs.append(p)
                elif i % 2 == 1:
                    h2_re_group = p
                    continue
                elif i % 2 == 0:
                    paragraphs.append(h2_re_group + p)
            paragraphs.append(gc_pagecontent_paragraphs[2])
        else:
            paragraphs.append(paragraphs_content[1])
#        paragraphs.extend(gc_pagecontent_re.split(paragraphs_content[1]))
#        for i, p in enumerate(line_re.split(paragraphs_content[1])):
#            if i == 0:
#                paragraphs.append(p)
#            elif i % 2 == 1:
#                line_re_group = p
#                continue
#            elif i % 2 == 0:
#                paragraphs.append(line_re_group + p)
        paragraphs.append(paragraphs_content[2])
        return paragraphs
    else:
        return paragraphs_content

def concat(paragraphs):
    return u"".join(p.original for p in paragraphs)

def compare(file_original, db_original, page = None):
    page_content_in_file = set(line.strip().lower() for line in file_original.decode('utf-8').splitlines())
    page_content_in_db = set(line.strip().lower() for line in db_original.splitlines())
    if page_content_in_file != page_content_in_db:
        raise ValidationError, u"content diff from content in db\n\n%s\n\n" % ("\n".join(page_content_in_file ^ page_content_in_db))
   
def concat_translations(translations):
    return u"".join(t for t in translations)
