# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView

from exams.models import Exam
from exams.forms import ExamForm


class ExamsList(ListView):

    model = Exam

    template_name = 'exams/exams_list.html'

    def get_queryset(self):

        # get original query set
        exams = super(ExamsList, self).get_queryset()

        # order exams list
        order_by = self.request.GET.get('order_by', '')

        # ordering exams by date by default
        exams = exams.order_by('date')

        if order_by in ('name', 'lector_name', 'date', 'exam_group', 'id'):
            exams = exams.order_by(order_by)
            if self.request.GET.get('reverse_lazy', '') == '1':
                exams = exams.reverse()

        return exams


# edit student controller
class ExamAddView(SuccessMessageMixin, CreateView):

    model = Exam

    template_name = 'exams/exams_add.html'

    form_class = ExamForm

    success_message = u"Іспит додано!"

    def get_success_url(self):
        return reverse_lazy('exams')

    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_button'):

            # send warning message
            messages.error(
                request,
                u'Додавання іспиту скасовано!')

            return HttpResponseRedirect(reverse_lazy('exams'))

        else:

            return super(ExamAddView, self).post(
                request,
                *args,
                **kwargs)


def exams_edit(request, eid):
    return HttpResponse('<h1>Edit Exam %s</h1>' % eid)


def exams_delete(request, eid):
    return HttpResponse('<h1>Delete Exam %s</h1>' % eid)
