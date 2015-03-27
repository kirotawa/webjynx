from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
    url(r'^main/?$', 'main', name='main'),
    url(r'^index/?$', 'main', name='main'),
    url(r'^addrepo/?$', 'addrepo', name='addrepo'),
)
