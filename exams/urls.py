from django.conf.urls import url

from exams.views import ExamAddView, ExamsList, exams_edit, exams_delete

urlpatterns = [
    url( r'^$', ExamsList.as_view(), name='exams'),
    url( r'^add/$', ExamAddView.as_view(), name='exams_add'),
    url( r'^(?P<eid>\d+)/edit/$', exams_edit, name='exams_edit'),
    url( r'^(?P<eid>\d+)/delete/$', exams_delete, name='exams_delete'),
]
