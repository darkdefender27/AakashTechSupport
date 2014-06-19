__author__ = 'shubham'

from django.conf.urls import patterns, include, url
from questions import views

urlpatterns = patterns(
    '',
    #url(r'^$', views.main, name='main'),

    url(r'^()$', views.all_questions_view, name='question'),
    #url(r'^tag/$', views.tag, name='tag'),
    url(r'^tags/$', views.view_tags, name='tags'),
    url(r'^tags/(?P<qid>\d+)/$', views.linktag, name='linktag'),
    url(r'^(qview/(?P<id>\d+))/$', views.qview, name='link'),
    url(r'^tag_search/$', views.tag_search, name='tag_search'),

)
