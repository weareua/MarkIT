from django.conf.urls import include, url

from exams.views import ExamAddView, ExamsList

urlpatterns = [
    url( r'^$', ExamsList.as_view(), name='exams'),
    url( r'^add/$', ExamAddView.as_view(), name='exams_add'),
    url( r'^(?P<eid>\d+)/edit/$', 'exams.views.exams_edit', name='exams_edit'),
    url( r'^(?P<eid>\d+)/delete/$', 'exams.views.exams_delete', name='exams_delete'),
]
