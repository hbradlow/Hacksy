from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('profiles.views',
    url(r'user/profile/$', "profile", name='profile'),
    url(r'ajax/profile_list/$', "ajax_profile_list", name='ajax_profile_list'),
    url(r'edit/(?P<username>[\w\d ]+)/$', "profile_edit", name='profile_edit'),
    url(r'(?P<username>[\w\d ]+)/$', "user_profile", name='user_profile'),
)
