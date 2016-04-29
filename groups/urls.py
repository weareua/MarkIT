from django.conf.urls import url

from groups.views import GroupDeleteView, groups_list, groups_add, groups_edit

urlpatterns = [
    url( r'^$', groups_list, name='groups'),
    url( r'^add/$', groups_add, name='groups_add'),
    url( r'^(?P<gid>\d+)/edit/$', groups_edit, name='groups_edit'),
    url( r'^(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(), name='groups_delete'),
]
