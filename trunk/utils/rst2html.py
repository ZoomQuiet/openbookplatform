from docutils.core import publish_parts
from docutils import nodes
from docutils.parsers.rst import directives
import re

g_style = {}

class highlight_block(nodes.General, nodes.Text):pass

from docutils.writers.html4css1 import Writer, HTMLTranslator

class SimpleWrite(Writer):
    def __init__(self):
        Writer.__init__(self)
        self.translator_class = SimpleHTMLTranslator
        
class SimpleHTMLTranslator(HTMLTranslator):
    def visit_highlight_block(self, node):
        self.body.append(node.astext())
    
    def depart_highlight_block(self, node):
        pass

def r_space(m):
    return len(m.group()) * '&nbsp;'

re_space = re.compile(r'^\s+', re.MULTILINE)
def code(name, arguments, options, content, lineno,
          content_offset, block_text, state, state_machine):
    global g_style
    
    lang = arguments[0]
    if not lang:
        lang = 'python'
    style, text = highlight(block_text[content_offset:], lang)
    text = re_space.sub(r_space, text)
    g_style[lang] = style
    return [highlight_block(text)]

code.content = 1
code.arguments = (1, 0, 1)
directives.register_directive('code', code)

def to_html(text, level=2):
    source = text
    parts = publish_parts(source, writer=SimpleWrite(), settings_overrides={'initial_header_level':level})
    if g_style:
        style = '<style>' + '\n'.join(g_style.values()) + '</style>'
    else:
        style = ''
    return  style + '\n' + parts['body']

def parts(file):
    fo = open(file, 'r')
    source = fo.read()
    fo.close()
    parts = publish_parts(source, source_path=file, writer_name='html')
    for k, v in parts.items():
        parts[k] = (v)
    return parts

def highlight(code, lang):
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    lexer = get_lexer_by_name(lang)
    return HtmlFormatter().get_style_defs('.highlight_'+lang), highlight(code, lexer, HtmlFormatter(cssclass='highlight_'+lang))

def rst2html(text):
    text = to_html(text)
    from BeautifulSoup import BeautifulSoup
    soup = BeautifulSoup(text)
    r_comment = re.compile(r'^\[(.*?)\]')
    max_id = 0
    tags = soup.findAll(['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'li', 'blockquote'])
    needs = []
    for t in tags:
        if t.name.startswith('h'):
            if t.a:
                t.contents = t.a.contents
        b = t.find(text=r_comment)
        if b:
            m = r_comment.match(b)
            b.replaceWith(b[m.end():])
            _id = m.group(1)
            if not _id:
                needs.append(t)
            else:
                max_id = max(int(_id), max_id)
                t['id'] = 'cn%d' % int(_id)
                t['class'] = 'cn'
    if needs:
        for t in needs:
            max_id += 1
            t['id'] = 'cn%d' % max_id
            t['class'] = 'cn'
#            t.contents[0].replaceWith(('[cn%d]' % max_id) + t.contents[0])
#            print t
    return str(soup)
    

if __name__ == '__main__':
    text = file('a.txt').read()
#    print '<html><head><title>test</title></head><body>%s</body></html>' % to_html(a)
    print rst2html(text)