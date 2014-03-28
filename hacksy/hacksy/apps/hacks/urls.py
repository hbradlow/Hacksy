from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('hacks.views',
    url(r'^awesome/(?P<slug>[\w\d\-_]+)/$', "awesome", name='awesome'),
    url(r'^unawesome/(?P<slug>[\w\d\-_]+)/$', "unawesome", name='unawesome'),
    url(r'^post/hack/$', "hack_create", name='hack_create'),
    url(r'^edit/(?P<slug>[\w\d\-_]+)/$', "hack_create", name='hack_edit'),
    url(r'^ajax/hack_list/$', 'ajax_hack_list', name='ajax_hack_list'),
    url(r'^ajax/hack_list/only/$', 'ajax_hack_list_only', name='ajax_hack_list_only'),
    url(r'^(?P<slug>[\w\d\-_]+)/$', "hack_detail", name='hack_detail'),
)
