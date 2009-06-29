# -*- coding: utf-8 -*-
import re
from django.template import Template, Context
from django.core.exceptions import ValidationError

def split(content, file_name = ''):
    body_content_re = re.compile(r'(<body.+?</body>)', flags = re.DOTALL)
    paragraphs_content = body_content_re.split(content)
    return paragraphs_content
#    len_contents = len(paragraphs_content)
#    print paragraphs_content
#    print len_contents
#    print contents
#    for content in contents:
#        print content
#    paragraphs_content = re.split(r"(\n{2,}[^\n]+?\n[-~=]+\n{2,})", content)

#    if len_contents == 1:
#        return [content, ]
#    elif len_contents == 3:
#        return [paragraphs_content[0] + '{{body_paragraph_content}}' + paragraphs_content[2], paragraphs_content[1]]

def concat(paragraphs):
    return u"".join(p.original for p in paragraphs)
#    paragraphs_count = len(paragraphs)
#    if paragraphs_count == 1:
#        return paragraphs[0].original
#    elif paragraphs_count == 2:
#        original1 = paragraphs[0].original
#        original2 = paragraphs[1].original
#        t = Template(original1)
#        c = Context({"body_paragraph_content": original2})
#        return  t.render(c)

def compare(file_original, db_original, page = None):
    page_content_in_file = set(line.strip().lower() for line in file_original.decode('utf-8').splitlines())
    page_content_in_db = set(line.strip().lower() for line in db_original.splitlines())
    if page_content_in_file != page_content_in_db:
        raise ValidationError, u"content diff from content in db\n\n%s\n\n" % ("\n".join(page_content_in_file ^ page_content_in_db))
   
def concat_translations(translations):
    return u"".join(t for t in translations)
