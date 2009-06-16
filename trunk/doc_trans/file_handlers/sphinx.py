# -*- coding: utf-8 -*-
import re
from django.core.exceptions import ValidationError

def split(content, file_name = ''):
    paragraphs_content = re.split(r"(\n{2,}[^\n]+?\n[-~=]+\n{2,})", content)
    result = []
    for i, paragraph_content in enumerate(paragraphs_content):
        if i == 0:
            result.append(paragraph_content.strip())
        elif i % 2 == 1:
            original_title = paragraph_content
            continue
        elif i % 2 == 0:
            result.append((original_title + paragraph_content).strip())
    return result

def concat(paragraphs):
    return u"\n\n".join(p.original for p in paragraphs)

def compare(file_original, db_original, page = None):
    page_content_in_file = set(line.strip().lower() for line in file_original.decode('utf-8').splitlines())
    page_content_in_db = set(line.strip().lower() for line in db_original.splitlines())
    if page_content_in_file != page_content_in_db:
        raise ValidationError, u"content diff from content in db\n\n%s\n\n" % ("\n".join(page_content_in_file ^ page_content_in_db))
    
def concat_translations(translations):
    return u"\n\n".join(t for t in translations)
