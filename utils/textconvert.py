#coding=utf-8
import re
import cgi

re_string = re.compile(r'(?P<htmlchars>[<&>])|(?P<space>^[ \t]+)|(?P<lineend>\r\n|\r|\n)|(?P<protocal>(^|\s)((http|ftp)://.*?))(\s|$)', re.S|re.M|re.I)
def plaintext2html(text, tabstop=4):
    def do_sub(m):
        c = m.groupdict()
        if c['htmlchars']:
            return cgi.escape(c['htmlchars'])
        if c['lineend']:
            return '<br>'
        elif c['space']:
            t = m.group().replace('\t', '&nbsp;'*tabstop)
            t = t.replace(' ', '&nbsp;')
            return t
        elif c['space'] == '\t':
            return ' '*tabstop;
        else:
            url = m.group('protocal')
            if url.startswith(' '):
                prefix = ' '
                url = url[1:]
            else:
                prefix = ''
            last = m.groups()[-1]
            if last in ['\n', '\r', '\r\n']:
                last = '<br>'
            return '%s<a href="%s">%s</a>%s' % (prefix, url, url, last)
    return re.sub(re_string, do_sub, text)

def bbcode(value):

    bbdata = [
        (r'\[url\](.+?)\[/url\]', r'<a href="\1">\1</a>'),
        (r'\[url=(.+?)\](.+?)\[/url\]', r'<a href="\1">\2</a>'),
        (r'\[email\](.+?)\[/email\]', r'<a href="mailto:\1">\1</a>'),
        (r'\[email=(.+?)\](.+?)\[/email\]', r'<a href="mailto:\1">\2</a>'),
        (r'\[img\](.+?)\[/img\]', r'<img src="\1">'),
        (r'\[img=(.+?)\](.+?)\[/img\]', r'<img src="\1" alt="\2">'),
        (r'\[b\](.+?)\[/b\]', r'<b>\1</b>'),
        (r'\[i\](.+?)\[/i\]', r'<i>\1</i>'),
        (r'\[u\](.+?)\[/u\]', r'<u>\1</u>'),
        (r'\[quote\](.+?)\[/quote\]', r'<blockquote>\1</blockquote>'),
        (r'\[center\](.+?)\[/center\]', r'<center>\1</center>'),
        (r'\[code\](.+?)\[/code\]', r'<pre>\1</pre>'),
        (r'\[big\](.+?)\[/big\]', r'<big>\1</big>'),
        (r'\[small\](.+?)\[/small\]', r'<small>\1</small>'),
        ]

    for bbset in bbdata:
        p = re.compile(bbset[0], re.DOTALL)
        value = p.sub(bbset[1], value)

    #The following two code parts handle the more complex list statements
    temp = ''
    p = re.compile(r'\[list\](.+?)\[/list\]', re.DOTALL)
    m = p.search(value)
    if m:
        items = re.split(re.escape('[*]'), m.group(1))
        for i in items[1:]:
            temp = temp + '<li>' + i + '</li>'
        value = p.sub(r'<ul>'+temp+'</ul>', value)

    temp = ''
    p = re.compile(r'\[list=(.)\](.+?)\[/list\]', re.DOTALL)
    m = p.search(value)
    if m:
        items = re.split(re.escape('[*]'), m.group(2))
        for i in items[1:]:
            temp = temp + '<li>' + i + '</li>'
        value = p.sub(r'<ol type=\1>'+temp+'</ol>', value)

    return value

def textformat(value, formattype=0):
    """formattype 0 html 1 plaintext 2 reST 3 bbcode"""
    if formattype == 0:
        return value
    elif formattype == 1:
        return plaintext2html(value)
    elif formattype == 2:
        try:
            from docutils.core import publish_parts
        except ImportError:
            return 'Convert text to reStructuredText error!'
        else:
            parts = publish_parts(source=value, writer_name="html4css1")
            return parts["fragment"]
    elif formattype == 3:
        from utils.textconvert import bbcode
        return bbcode(value)
    else:
        return value

def truncatestr(value, length=100, encoding='utf-8'):
    if not value:
        return ''
    if isinstance(value, str):
        text = unicode(value, encoding, 'ignore')
    else:
        text = value
    j = 0
    i = 0
    for i, c in enumerate(text):
        if j >= length:
            break
        if ord(c) > 127:
            j += 2
        else:
            j += 1
    t = text[:i+1].encode(encoding)
    if len(t) == len(value):
        suffix = ''
    else:
        suffix = '...'
    return t + suffix

if __name__ == '__main__':
    text="""aabhttp://www.example.com http://www.example.com
http://www.example.com <<< [<aaaa></aaaa>]
"""
    print plaintext2html(text)
    