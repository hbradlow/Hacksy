from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('blog.views',
    url(r'^$', "blogpost_list", name='blog'),
    url(r'^(?P<slug>[\w\d\-_]+)/$', "blogpost_detail", name='blogpost_detail'),
)
