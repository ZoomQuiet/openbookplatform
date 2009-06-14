from Captcha.Visual import Text, Backgrounds, Distortions
from Captcha import Words
import random
import Image
from cStringIO import StringIO

class BaseRender(object):
    defaultSize = (100,30)
    defaultfontfactory = Text.FontFactory(20, "vera")
    
    def __init__(self):
        self.fontfactory = None
        self._word = None

    def render(self, word=None, size=None):
        if size is None:
            size = self.defaultSize
        if not word:
            word = self.word
        return word, self.__do_render(self.get_layers(word), Image.new("RGB", size))
    
    def get_layers(self, word):
        return self.renderlist
    
    def set_font_factory(self, factory):
        self.fontfactory = factory
        
    def get_font_factory(self):
        if not self.fontfactory:
            return self.defaultfontfactory
        return self.fontfactory
    
    def __get_word(self):
        if not self._word:
            self._word = Words.defaultWordList.pick()
        return self._word
    
    word = property(__get_word)

    def __do_render(self, _list, img):
        for i in _list:
            if isinstance(i, (tuple, list)):
                img = self.__do_render(img)
            else:
                img = i.render(img) or img
        return img
    
#    def get_color(self):
#        textcolor = random.randint(0, 255)
#        bordercolor = 255 - textcolor
#        return textcolor, bordercolor
#
class PseudoGimpy(BaseRender):
    def get_layers(self, word):
        return [
            random.choice([
                Backgrounds.CroppedImage(),
                Backgrounds.TiledImage(),
            ]),
            Text.TextLayer(word, borderSize=1, fontFactory=self.get_font_factory()),
            Distortions.SineWarp(),
            ]


class AngryGimpy(BaseRender):
    def get_layers(self, word):
        return [
            Backgrounds.TiledImage(),
            Backgrounds.RandomDots(),
            Text.TextLayer(word, borderSize=1, fontFactory=self.get_font_factory()),
#            Distortions.WigglyBlocks(),
            ]


class AntiSpam(BaseRender):
    fontFactory = Text.FontFactory(20, "vera/VeraBd.ttf")

    def get_layers(self, word):
        textLayer = Text.TextLayer(word,
                                   borderSize = 1,
                                   fontFactory = self.fontFactory)

        return [
            Backgrounds.CroppedImage(),
            textLayer,
            Distortions.SineWarp(amplitudeRange = (2, 4)),
            ]

def get_image(word=None, style='pseudo', size=None, filetype='JPEG'):
    if style == 'pseudo':
        cls = PseudoGimpy
    elif style == 'angry':
        cls = AngryGimpy
    elif style == 'antispam':
        cls = AntiSpam
    else:
        cls = AntiSpam
    obj = cls()
    word, img = obj.render(word)
    buf = StringIO()
    img.save(buf, filetype)
    return word, buf.getvalue()

def valid_obj(word=None, style='pseudo', size=None):
    if style == 'pseudo':
        cls = PseudoGimpy
    elif style == 'angry':
        cls = AngryGimpy
    elif style == 'antispam':
        cls = AntiSpam
    else:
        cls = AntiSpam
    obj = cls()
    return obj

#django binding
from django.conf import settings
from django.core.cache import cache
import base64
import md5
import time

TIMEOUT = 5*60

def create_key():
    word = valid_obj().word
    date = time.strftime("%Y%m%d%H%M%S")
    d = md5.new(word + date + settings.SECRET_KEY).hexdigest()
    w = base64.standard_b64encode(word)
    return w + date + d

def get_word(key):
    try:
        d = key[-32:]
        date = key[-46:-32]
        w = key[:len(key)-46]
        #judge the time
        t = time.mktime(time.strptime(date, "%Y%m%d%H%M%S"))
        if 0 <= time.time() - t <= TIMEOUT:
            word = base64.standard_b64decode(w)
            nd = md5.new(word + date + settings.SECRET_KEY).hexdigest()
            if nd == d:
                return word
    except:
        import traceback
        traceback.print_exc()
        pass
    return False

def valid_key(key, word):
    k = get_word(key)
    if k:
        flag = k == word
        if flag:
            #check if the cache has the key, if has the key should be invalid
            if cache.get(word):
                return False
            else:
                #set to cache
                cache.set(word, 1, TIMEOUT)
                return True
    else:
        return False
    
if __name__ == '__main__':
    word, img = get_image(style='pseudo')
    print word
    img.save('a.jpg', 'JPEG')
    word, img = get_image(style='angry')
    print word
    img.save('b.jpg', 'JPEG')
    word, img = get_image(style='antispam')
    print word
    img.save('c.jpg', 'JPEG')
    
    