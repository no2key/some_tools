from django.conf.urls import patterns, include, url
from WinTool.views import *
from WinTool.auth import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r"^$", index),
    url(r"change_password", change_password),
    url(r"do_update/", do_update),
    url(r"do_change_pass/", do_change_pass),
    url(r"details/(?P<pk>\d+)", get_detail),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
)
