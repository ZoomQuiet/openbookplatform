from django.conf.urls.defaults import *

urlpatterns = patterns('apps.users.views.groupview',

    (r'^$', 'group_list'),
    (r'^add/$', 'group_add'),
    (r'^(?P<group_id>\d+)/$', 'group_detail'),
    (r'^(?P<group_id>\d+)/edit/$', 'group_edit'),
    (r'^(?P<group_id>\d+)/delete/$', 'group_delete'),
    (r'^(?P<group_id>\d+)/join/$', 'group_join'),
    (r'^(?P<group_id>\d+)/addmember/$', 'group_addmember'),
    (r'^(?P<group_id>\d+)/delmember/(?P<object_id>\d+)/$', 'group_delmember'),
)

import apps.document.views
from utils.decorator import template, json, ajax_iframe_response
from models import Group
from decorator import add_group, get_topic, get_owner_and_topic

d_list = template('users/group_document.html')
d_edit = template('users/group_document_detail.html')
d_tag = template('users/group_document_tag.html')

para = {'model':Group, 'url':'group'}
urlpatterns += patterns('',
    (r'^(?P<object_id>\d+)/document/$', d_list(add_group(apps.document.views.list)), para),
    (r'^(?P<object_id>\d+)/document/addfile/$', ajax_iframe_response(apps.document.views.addfile), para),
    (r'^(?P<object_id>\d+)/document/list/$', 'apps.document.views.ajax_list', para),
    (r'^(?P<object_id>\d+)/document/taglist/$', 'apps.document.views.ajax_taglist', para),
    (r'^(?P<object_id>\d+)/document/delete/$', 'apps.document.views.delete', para),
    (r'^(?P<object_id>\d+)/document/(?P<doc_id>\d+)/edit/$', d_edit(add_group(apps.document.views.edit)), para),
    (r'^(?P<object_id>\d+)/document/(?P<doc_id>\d+)/delete/$', 'apps.document.views.delete', para),
    (r'^(?P<object_id>\d+)/document/tag/(?P<tag_id>\d+)/delete/$', 'apps.document.views.deletetag', para),
    (r'^(?P<object_id>\d+)/document/tag/(?P<tag_id>\d+)/list/$', 'apps.document.views.ajax_tagfilelist', para),
    (r'^(?P<object_id>\d+)/document/tag/(?P<tag_id>\d+)/$', d_tag(add_group(apps.document.views.tag)), para),
)

import apps.forum.views
import apps.tag.views
import apps.comment.views

f_list = template('users/group_forum.html')
f_topic = template('users/group_forum_topic.html')
f_tag = template('users/group_forum_tag.html')
urlpatterns += patterns('',
    (r'^(?P<group_id>\d+)/forum/$', f_list(add_group(apps.forum.views.list))),
    (r'^(?P<group_id>\d+)/forum/list/$', 'apps.forum.views.ajax_list'),
    (r'^(?P<group_id>\d+)/forum/taglist/$', json(apps.tag.views.list), {'model':Group, 'type':'forum'}),
    (r'^(?P<group_id>\d+)/forum/add/$', 'apps.forum.views.add'),
    (r'^(?P<group_id>\d+)/forum/topic/(?P<topic_id>\d+)/$', f_topic(add_group(apps.forum.views.topic))),
    (r'^(?P<group_id>\d+)/forum/topic/(?P<topic_id>\d+)/comment/$', json(get_topic(apps.comment.views.list))),
    (r'^(?P<group_id>\d+)/forum/topic/(?P<topic_id>\d+)/addcomment/$', get_owner_and_topic(apps.comment.views.addcomment)),
#    (r'^(?P<group_id>\d+)/forum/tag/(?P<tag_id>\d+)/delete/$', 'apps.document.views.deletetag', para),
    (r'^(?P<group_id>\d+)/forum/tag/(?P<tag_id>\d+)/list/$', 'apps.forum.views.taglist'),
    (r'^(?P<group_id>\d+)/forum/tag/(?P<tag_id>\d+)/$', f_tag(apps.forum.views.tag)),
)

from apps.task.models import Task
import apps.task.views

t_list = template('task/task.html')
urlpatterns += patterns('',
    (r'^(?P<object_id>\d+)/task/$', t_list(add_group(apps.task.views.list)), {'model':Task}),
)
