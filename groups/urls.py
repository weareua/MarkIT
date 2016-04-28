from django.conf.urls import include, url

from groups.views import GroupDeleteView

urlpatterns = [
    url( r'^$', 'groups.views.groups_list', name='groups'),
    url( r'^add/$', 'groups.views.groups_add', name='groups_add'),
    url( r'^(?P<gid>\d+)/edit/$', 'groups.views.groups_edit', name='groups_edit'),
    url( r'^(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(), name='groups_delete'),
]
