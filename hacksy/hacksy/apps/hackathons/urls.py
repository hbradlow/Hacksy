from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('hackathons.views',
    url(r'^$', "hackathon_list", name='hackathon_list'),
    url(r'^host/', direct_to_template, {"template":"hackathons/host.html"}, name='host'),
    url(r'^ajax_hackathon_list/', 'ajax_hackathon_list', name='ajax_hackathon_list'),

    url(r'^hackathon/csv/(?P<slug>[\w\d\-_]+)/$', "hackathon_csv", name='hackathon_csv'),

    url(r'^hackathon/(?P<slug>[\w\d\-_]+)/$', "hackathon_detail", name='hackathon_detail'),
    url(r'^team/dashboard/(?P<slug>[\w\d\-_]+)/$', "team_detail", name='team_detail'),
    url(r'^dashboard/(?P<slug>[\w\d\-_]+)/$', "dashboard", name='dashboard'),

    url(r'^create/$', "hackathon_create", name='hackathon_create'),
    url(r'^edit/(?P<slug>[\w\d\-_]+)/$', "hackathon_create", name='hackathon_edit'),

    url(r'^team/create/$', "team_create", name='team_create'),
    url(r'^team/edit/(?P<slug>[\w\d\-_]+)/$', "team_create", name='team_edit'),


    url(r'^judge/edit/(?P<hackathon_slug>[\w\d\-_]+)/$', "judge_edit", name='judge_edit'),
    url(r'^sponsor/edit/(?P<hackathon_slug>[\w\d\-_]+)/$', "sponsor_edit", name='sponsor_edit'),
    url(r'^prize/edit/(?P<hackathon_slug>[\w\d\-_]+)/$', "prize_edit", name='prize_edit'),
)
