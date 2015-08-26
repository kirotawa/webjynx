from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'core.views',
    url(r'^/?$', 'login', name='login'),
    url(r'^main/(?P<user_id>\d+)/?$', 'main', name='main'),
    url(r'^index/?$', 'main', name='main'),
    url(r'^addrepo/?$', 'addrepo', name='addrepo'),
    url(r'^login/?$', 'login', name='login'),
    url(r'^logout/?$', 'logout', name='logout'),
    url(r'^register/?$', 'register', name='register'),
)
