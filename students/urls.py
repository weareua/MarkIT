from django.conf.urls import url

from students.views import StudentUpdateView, StudentDeleteView, students_add

urlpatterns = [
    url( r'^add/$', students_add, name='students_add'),
    url(r'^(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
    url(r'^(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),

]
