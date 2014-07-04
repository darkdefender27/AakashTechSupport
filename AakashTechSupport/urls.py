__author__ = 'ushubham27'

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'AakashTechSupport.views.home', name='home'),
    # url(r'^AakashTechSupport/', include('AakashTechSupport.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^admin/', include(admin.site.urls)),

    url(r'^aakashuser/', include('aakashuser.urls')),
    url(r'^questions/', include('questions.urls')),
    url(r'^ticketing/', include('ticketing.urls')),


    url(r'^$', 'aakashuser.views.index', name='indexpage'),
    url(r'^register/$', 'aakashuser.views.register', name='register'),
    url(r'^login/$', 'aakashuser.views.login_new', name='login_new'),
    url(r'^logout/$', 'aakashuser.views.logout_new', name='logout_new'),
    url(r'^index/$', 'aakashuser.views.index', name='index'),
    url(r'^search/$', 'aakashuser.views.search', name='index'),
               (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),
)

handler404 = 'aakashuser.views.handler404'