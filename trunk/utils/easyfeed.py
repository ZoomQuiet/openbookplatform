from django.core.exceptions import ObjectDoesNotExist
from django.utils import feedgenerator
from django.conf import settings

def add_domain(domain, url, prefix):
    if url.startswith('/'):
        url = url[1:]
    if not url.startswith('http://'):
        if prefix:
            url = u'%s/%s/%s' % (domain, prefix, url)
        else:
            url = u'%s/%s' % (domain, url)
    return url

def get_dynamic_attr(obj, attname, default=None):
    try:
        attr = getattr(obj, attname)
    except AttributeError:
        return default
    if callable(attr):
        return attr()
    return attr

class FeedDoesNotExist(ObjectDoesNotExist):
    pass

class EasyFeed(object):
    item_pubdate = None
    item_enclosure_url = None
    feed_type = feedgenerator.DefaultFeed

    def __init__(self, domain, feed_url, prefix=''):
        self.domain = domain
        if not self.domain.startswith('http://'):
            self.domain = 'http://' + self.domain
        if self.domain.endswith('/'):
            self.domain = self.domain[:-1]
        self.feed_url = feed_url
        self.prefix = prefix

    def get_feed(self):
        """
        Returns a feedgenerator.DefaultFeed object, fully populated, for
        this feed. Raises FeedDoesNotExist for invalid parameters.
        """
        feed = self.feed_type(
            title = get_dynamic_attr(self, 'title'),
            link = add_domain(self.domain, get_dynamic_attr(self, 'link'), self.prefix),
            description = get_dynamic_attr(self, 'description'),
            language = settings.LANGUAGE_CODE.decode(),
            feed_url = add_domain(self.domain, self.feed_url, self.prefix),
            author_name = get_dynamic_attr(self, 'author_name'),
            author_link = get_dynamic_attr(self, 'author_link'),
            author_email = get_dynamic_attr(self, 'author_email'),
        )

        for item in self.items():
            link = add_domain(self.domain, get_dynamic_attr(item, 'rss_link'), self.prefix)
            enc = None
            enc_url = get_dynamic_attr(item, 'rss_enclosure_url')
            if enc_url:
                enc = feedgenerator.Enclosure(
                    url = enc_url.decode('utf-8'),
                    length = str(get_dynamic_attr(item, 'rss_enclosure_length')).decode('utf-8'),
                    mime_type = self.__get_dynamic_attr(item, 'rss_enclosure_mime_type').decode('utf-8'),
                )
            author_name = get_dynamic_attr(item, 'rss_author_name')
            if author_name is not None:
                author_email = get_dynamic_attr(item, 'rss_author_email')
                author_link = get_dynamic_attr(item, 'rss_author_link')
            else:
                author_email = author_link = None
            feed.add_item(
                title = get_dynamic_attr(item, 'rss_title'),
                link = link,
                description = get_dynamic_attr(item, 'rss_description'),
                unique_id = link,
                enclosure = enc,
                pubdate = get_dynamic_attr(item, 'rss_pubdate'),
                author_name = get_dynamic_attr(item, 'rss_author_name'),
                author_email = get_dynamic_attr(item, 'rss_author_email'),
                author_link = get_dynamic_attr(item, 'rss_author_link'),
            )
            print 'author_name=', item, get_dynamic_attr(item, 'rss_author_name')
        return feed

    def items(self):
        raise Exception, 'Not Implemented'
