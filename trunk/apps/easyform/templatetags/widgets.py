from apps.easyform.enhancedtag import EnhancedLibrary

register = EnhancedLibrary()

def button(value):
    return {'button_value':value}
register.inclusion_tag('easyform/button.html')(button)

def submitbutton(value):
    return {'button_value':value}
register.inclusion_tag('easyform/submitbutton.html')(submitbutton)

def alink(link, label, title=''):
    return {'href':link, 'title':title, 'label':label}
register.inclusion_tag('easyform/alink.html')(alink)

