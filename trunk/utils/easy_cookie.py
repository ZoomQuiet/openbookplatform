from django.conf import settings
import datetime

def set_cookie(response, key, value):
    max_age = settings.SESSION_COOKIE_AGE
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=365*24*60*60), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, 
        domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)
    