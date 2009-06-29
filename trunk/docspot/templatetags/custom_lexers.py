# -*- coding: utf-8 -*-
from pygments.lexer import RegexLexer
from pygments.lexers.web import HtmlLexer
from pygments.lexers.agile import RubyLexer
from pygments.lexers.text import YamlLexer
from pygments.lexers.special import TextLexer
from pygments.token import *
from pygments.lexer import RegexLexer, bygroups, using
import re

class TextileLexer(RegexLexer):
    name = 'Textile'
    aliases = ['textile']
    filenames = ['*.textile']
    
    flags = re.IGNORECASE | re.DOTALL
    tokens = {
        'root': [
            
            (r'(h[1-6]\.)(.+?)\n', bygroups(Keyword, Generic.Heading)),
#            (r'(\*)(.+?)\n', bygroups(Keyword, Text)),
            (r'(\+)([^\n]+?)(\+)', bygroups(Punctuation, Generic.Strong, Punctuation)),
            (r'<\s*ruby\s*', Name.Tag, 'ruby-code',),
            (r'<\s*yaml\s*', Name.Tag, 'yaml-code',),
            (r'<\s*shell\s*', Name.Tag, 'shell-code',),
            (r'<\s*[a-zA-Z0-9:]+>', Name.Tag,),
            (r'<\s*/\s*[a-zA-Z0-9:]+\s*>', Name.Tag),
            (r'.', Text),
        ],
        'ruby-code': [
            (r'(.+?)(<\s*/\s*ruby\s*>)',
             bygroups(using(RubyLexer), Name.Tag),
             '#pop'),
        ],
        'yaml-code': [
            (r'(.+?)(<\s*/\s*yaml\s*>)',
             bygroups(using(YamlLexer), Name.Tag),
             '#pop'),
        ],
        'shell-code': [
            (r'(.+?)(<\s*/\s*shell\s*>)',
             bygroups(using(TextLexer), Name.Tag),
             '#pop'),
        ]
    }
