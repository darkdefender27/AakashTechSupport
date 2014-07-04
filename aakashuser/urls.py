#Define your urls here.
__author__ = 'ushubham27'

from django.conf.urls import patterns, url, include

urlpatterns = patterns('',

    #url(r'^questions/$', 'aakashuser.views.display_questions', name='index'),
    #url(r'^tags/$', 'aakashuser.views.view_tags', name='tags'),
    #url(r'^search/$', 'aakashuser.views.search_tags', name='search_tags'),
    url(r'^profile/$', 'aakashuser.views.profile', name='profile'),	
    url(r'^view_profile/$', 'aakashuser.views.view_profile', name='view profile'),
    url(r'^view_profile/questions/$', 'aakashuser.views.view_profile', name='view profile'),
    url(r'^view_profile/answers/$', 'aakashuser.views.view_related_answers', name='view_profile_related_ans'),
    url(r'^reset/$', 'aakashuser.views.reset', name='reset_password'),
    url(r'^change/$', 'aakashuser.views.change', name='reset_password'),


)
