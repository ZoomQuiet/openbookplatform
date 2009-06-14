from django.conf.urls.defaults import *
from django.contrib.auth.models import User

urlpatterns = patterns('apps.users.views.views',

    (r'^$', 'userlist'),
    (r'^(?P<object_id>\d+)/$', 'user_detail'),
    (r'^(?P<object_id>\d+)/edit/$', 'user_edit'),
    (r'^(?P<object_id>\d+)/saveportrait/$', 'user_save_portrait'),
#    (r'^(?P<object_id>\d+)/document/', include('apps.document.iurls'), {'model':User, 'url':'user'}),
    (r'^delete/$', 'user_delete_multi'),
    (r'^(?P<object_id>\d+)/delete/$', 'user_delete'),
    (r'^addsysmanager/$', 'user_addsysmanager_multi'),
    (r'^(?P<object_id>\d+)/addsysmanager/$', 'user_addsysmanager'),
    (r'^(?P<object_id>\d+)/removesysmanager/$', 'user_removesysmanager'),
)

import apps.document.views
from utils.decorator import template, ajax_iframe_response
from decorator import add_person

d_list = template('users/user_document.html')
d_edit = template('users/user_document_detail.html')
d_tag = template('users/user_document_tag.html')

para = {'model':User, 'url':'user'}
urlpatterns += patterns('',
    (r'^(?P<object_id>\d+)/document/$', d_list(add_person(apps.document.views.list)), para),
    (r'^(?P<object_id>\d+)/document/addfile/$', ajax_iframe_response(apps.document.views.addfile), para),
    (r'^(?P<object_id>\d+)/document/list/$', 'apps.document.views.ajax_list', para),
    (r'^(?P<object_id>\d+)/document/taglist/$', 'apps.document.views.ajax_taglist', para),
    (r'^(?P<object_id>\d+)/document/delete/$', 'apps.document.views.delete', para),
    (r'^(?P<object_id>\d+)/document/(?P<doc_id>\d+)/edit/$', d_edit(add_person(apps.document.views.edit)), para),
    (r'^(?P<object_id>\d+)/document/(?P<doc_id>\d+)/delete/$', 'apps.document.views.delete', para),
    (r'^(?P<object_id>\d+)/document/tag/(?P<tag_id>\d+)/delete/$', 'apps.document.views.deletetag', para),
    (r'^(?P<object_id>\d+)/document/tag/(?P<tag_id>\d+)/list/$', 'apps.document.views.ajax_tagfilelist', para),
    (r'^(?P<object_id>\d+)/document/tag/(?P<tag_id>\d+)/$', d_tag(add_person(apps.document.views.tag)), para),
)

import apps.newmessage.views

m_list = template('users/user_message.html')
urlpatterns += patterns('',
    (r'^(?P<object_id>\d+)/message/$', m_list(add_person(apps.newmessage.views.list))),
    (r'^(?P<object_id>\d+)/message/list/$', 'apps.newmessage.views.ajax_list'),
    (r'^(?P<object_id>\d+)/message/delete/$', 'apps.newmessage.views.delete'),
#    (r'^(?P<object_id>\d+)/message/(?P<message_id>\d+)/delete/$', 'apps.newmessage.views.delete'),
    (r'^(?P<object_id>\d+)/message/send/$', 'apps.newmessage.views.send'),
)
