from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^$', 'apps.portal.views.index'),
    (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': settings.SITE_MEDIA}),

    (r'^admin/', include('django.contrib.admin.urls')),
)
