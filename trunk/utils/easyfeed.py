from django.utils import feedgenerator
from django.conf import settings
from django.http import HttpResponse
from django.utils.feedgenerator import Atom1Feed

def render_feed(feed):
    feedgen = feed.get_feed()
    response = HttpResponse(mimetype=feedgen.mime_type)
    feedgen.write(response, 'utf-8')
    return response

def add_domain(domain, url, prefix):
    if url.startswith('/'):
        url = url[1:]
    if not url.startswith('http://'):
        if prefix:
            url = u'%s/%s/%s' % (domain, prefix, url)
        else:
            url = u'%s/%s' % (domain, url)
    return url

class EasyFeed(object):
    item_pubdate = None
    item_enclosure_url = None
    feed_type = Atom1Feed

    def __init__(self, feed_url, domain='', prefix=''):
        self.domain = domain
        if not self.domain:
            import urlparse
            v = urlparse.urlparse(feed_url)
            self.domain = v[0] + '://' + v[1]
        if not self.domain.startswith('http://'):
            self.domain = 'http://' + self.domain
        if self.domain.endswith('/'):
            self.domain = self.domain[:-1]
        self.feed_url = feed_url
        self.prefix = prefix

    def __get_dynamic_attr(self, attname, obj=None, default=None):
        value = ''
        try:
            attr = getattr(self, attname)
        except AttributeError:
            value = default
        else:
            if callable(attr):
                # Check func_code.co_argcount rather than try/excepting the
                # function and catching the TypeError, because something inside
                # the function may raise the TypeError. This technique is more
                # accurate.
                if hasattr(attr, 'func_code'):
                    argcount = attr.func_code.co_argcount
                else:
                    argcount = attr.__call__.func_code.co_argcount
                if argcount == 2: # one argument is 'self'
                    value = attr(obj)
                else:
                    value = attr()
        if isinstance(value, str):
            value = unicode(value, settings.DEFAULT_CHARSET)

        return value
    
    def get_feed(self):
        """
        Returns a feedgenerator.DefaultFeed object, fully populated, for
        this feed. 
        """
        feed = self.feed_type(
            title = self.__get_dynamic_attr('title'),
            link = add_domain(self.domain, self.__get_dynamic_attr('link', default=''), self.prefix),
            description = self.__get_dynamic_attr('description'),
            language = settings.LANGUAGE_CODE.decode(),
            feed_url = add_domain(self.domain, self.feed_url, self.prefix),
            author_name = self.__get_dynamic_attr('author_name'),
            author_link = self.__get_dynamic_attr('author_link'),
            author_email = self.__get_dynamic_attr('author_email'),
        )

        for item in self.items():
            link = add_domain(self.domain, self.__get_dynamic_attr('item_link', item), self.prefix)
            enc = None
            enc_url = self.__get_dynamic_attr('item_enclosure_url', item)
            if enc_url:
                enc = feedgenerator.Enclosure(
                    url = enc_url.decode('utf-8'),
                    length = str(self.__get_dynamic_attr('item_enclosure_length', item)).decode('utf-8'),
                    mime_type = self.__get_dynamic_attr('item_enclosure_mime_type', item).decode('utf-8'),
                )
            author_name = self.__get_dynamic_attr('item_author_name', item)
            if author_name is not None:
                author_email = self.__get_dynamic_attr('item_author_email', item)
                author_link = self.__get_dynamic_attr('item_author_link', item)
            else:
                author_email = author_link = None
            print item, 'name=', author_name
            feed.add_item(
                title = self.__get_dynamic_attr('item_title', item),
                link = link,
                description = self.__get_dynamic_attr('item_description', item),
                unique_id = link,
                enclosure = enc,
                pubdate = self.__get_dynamic_attr('item_pubdate', item),
                author_name = author_name,
                author_email = author_email,
                author_link = author_link,
            )
        return feed

    def items(self):
        raise Exception, 'Not Implemented'
