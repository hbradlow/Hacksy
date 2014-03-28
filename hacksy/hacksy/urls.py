from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    #specific urls
    url(r'',include('social_auth.urls')),
    url(r'^$', "hacks.views.home", name='home'),
    url(r'^signin/', direct_to_template, {"template":"registration/login.html"}, name='signin'),
    url(r'^logout/',  'django.contrib.auth.views.logout', {"next_page": "/"},name="logout"),
    url(r'login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'register/$', 'profiles.views.user_create', name="register"),

    # Static pages
    url(r'^terms/', direct_to_template, {"template":"footer/terms.html"}, name='terms'),
    url(r'^privacy/', direct_to_template, {"template":"footer/privacy.html"}, name='privacy'),
    url(r'^contact/', direct_to_template, {"template":"contact.html"}, name='contact'),

    # Currently not in use
    url(r'^browse/', direct_to_template, {"template":"browse.html"}, name='browse'),

    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    #apps
    url(r'^hackers/',include('profiles.urls')),
    url(r'^hacks/',include('hacks.urls')),
    url(r'^hackathons/',include('hackathons.urls')),
    url(r'^comments/', include('comments.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^blog/', include('blog.urls')),

    #hackathon
    url(r'^(?P<slug>[\w\d\-_]+)/$',  'hackathons.views.hackathon_detail', name="hackathon_detail"),

    # favicon
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': 'http://s3.amazonaws.com/hacksy/favicon3.png'}),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
