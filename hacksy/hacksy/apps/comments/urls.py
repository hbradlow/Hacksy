from django.conf.urls import patterns, url

urlpatterns = patterns('comments.views',
    url(r'^post/$',          'comments.post_comment',       name='comments-post-comment'),
    url(r'^ajax_post/$',          'comments.ajax_post_comment',       name='ajax-comments-post-comment'),
    url(r'^ajax_remove_post/(?P<comment_pk>.+)/$',          'comments.ajax_remove_post_comment',       name='ajax-comments-post-comment-remove'),
    url(r'^posted/$',        'comments.comment_done',       name='comments-comment-done'),
    url(r'^flag/(\d+)/$',    'moderation.flag',             name='comments-flag'),
    url(r'^flagged/$',       'moderation.flag_done',        name='comments-flag-done'),
    url(r'^delete/(\d+)/$',  'moderation.delete',           name='comments-delete'),
    url(r'^deleted/$',       'moderation.delete_done',      name='comments-delete-done'),
    url(r'^approve/(\d+)/$', 'moderation.approve',          name='comments-approve'),
    url(r'^approved/$',      'moderation.approve_done',     name='comments-approve-done'),

    url(r"^vote/(?P<object_id>.+)/(?P<vote>\d+)/$", "comments.vote", name="vote"),


)

urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='comments-url-redirect'),
)
