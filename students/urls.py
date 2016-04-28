from django.conf.urls import include, url

from students.views import StudentUpdateView, StudentDeleteView

urlpatterns = [
    url( r'^add/$', 'students.views.students_add', name='students_add'),
    url(r'^(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
    url(r'^(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),

]
