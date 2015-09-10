from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.ClientRedirectView.as_view(), name='entries-root'),
    url(r'^clients/$', views.ClientCreateView.as_view(), name='client-list'),
    url(r'^clients/(?P<pk>\d+)/$', views.ClientUpdateView.as_view(),
        name='client-detail'),
    url(r'^entries/$', views.EntryCreateView.as_view(), name='entry-list'),
    url(r'^projects/$', views.ProjectCreateView.as_view(),
        name='project-list'),
    url(r'^projects/(?P<pk>\d+)/$', views.ProjectUpdateView.as_view(),
        name='project-detail'),
    # Auth urls
    url(r'^auth/login/$', auth_views.login, {'template_name': 'auth/login.html'}),
    url(r'^auth/logout/$', auth_views.logout, {'next_page': '/'}),
]
