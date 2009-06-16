# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe

register = template.Library()
from pygments import highlight as highlight_handler
from pygments.lexers.text import RstLexer
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from django.utils.html import escape
from django.utils.text import wrap
from doc_trans.models import Translation, Paragraph, Page
from doc_trans.settings import LEXER_NAME_MAP
from doc_trans.templatetags.custom_lexers import TextileLexer

@register.filter
def linediff(value, old_value):
    value_set = set(value.splitlines())
    old_value_set = set(old_value.splitlines())
    only_in_value = value_set - old_value_set
    result = []
    for line in value.splitlines():
        if line in only_in_value:
            line = '<span style = "background-color:#E1E1E1">%s</span>' % escape(line)
        else:
            line = escape(line)
        result.append(line)
    return mark_safe("\n".join(result))


@register.filter
def highlight(value):
    if isinstance(value, Paragraph):
        content = value.original
        lexer_name = LEXER_NAME_MAP[value.page.doc_type]
    elif isinstance(value, Translation):
        content = value.content
        lexer_name = LEXER_NAME_MAP[value.paragraph.page.doc_type]
    if lexer_name == 'textile':
        lexer = TextileLexer()
#        return mark_safe(u"<pre>%s</pre>" % escape(content))
    else:
        lexer = get_lexer_by_name(lexer_name)
    return mark_safe(highlight_handler(content, lexer, HtmlFormatter()))

@register.filter
def level_to_url(value):
    return "../" * value