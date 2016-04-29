# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from students.models import Student
from groups.models import Group
from students.forms import StudentUpdateForm
from MarkIT.util import get_current_group, paginate


def students_list(request):

    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:
        # otherwise show all students
        students = Student.objects.all()

    # try to order students list
    order_by = request.GET.get('order_by', ' ')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', ' ') == '1':
            students = students.reverse()

    # apply pagination, 15 students per page
    context = paginate(students, 15, request, {}, var_name = 'students')

    return render(request, 'students_list.html', context)

@login_required
def students_add(request):

    # was form posted?
    if request.method == "POST":

        # was form "add" button clicked?
        if request.POST.get('add_button') is not None:

            # validate input data
            errors = {}

            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            # verify user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім’я є обов’язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов’язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження обов’язкова"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = \
                        'Введіть коректний формат дати (напр. 1988-12-30)'
                data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета обов’язковий"
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u'Маєте обрати групу для студента'
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = 'Оберіть коректну групу'
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                correct_image = valid_image_mimetype(photo)
                if correct_image:
                    data['photo'] = photo
                else:
                    errors['photo'] = u"Оберіть зображення"

            # save student
            if not errors:

                student = Student(**data)
                student.save()

                # send success message
                messages.success(
                    request,
                    u"Студент %s %s успішно доданий в базу обліку."
                    % (student.first_name, student.last_name)
                    )

                # redirect user to students list
                return HttpResponseRedirect(reverse('home'))

            else:

                # send error message
                messages.error(
                    request,
                    u'Будь ласка, заповність форму корректно')

                # render form with errors and previous user input
                return render(
                    request,
                    'students/students_add.html',
                    {'groups': Group.objects.all().order_by('title'),
                     'errors': errors})

        elif request.POST.get('cancel_button') is not None:

            # send warning message
            messages.error(
                request,
                u'Додавання студента скасовано!')

            # redirect to home page on cancel button
            return HttpResponseRedirect(reverse('home'))

    else:
        # return user to form
        return render(
            request,
            'students_add.html',
            {'groups': Group.objects.all().order_by('title')})


# edit student controller
class StudentUpdateView(SuccessMessageMixin, UpdateView):
    model = Student
    template_name = 'students_edit.html'
    form_class = StudentUpdateForm

    success_message = u"Зміни збережено."

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('home')

    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_button'):

            # send warning message
            messages.error(
                request,
                u'Редагування студента скасовано!')

            return HttpResponseRedirect(reverse('home'))

        else:
            return super(StudentUpdateView, self).post(
                request,
                *args,
                **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students_confirm_delete.html'
    success_url = reverse_lazy('home')
    success_message = u"Студент видалений успішно."

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentDeleteView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(StudentDeleteView, self).delete(
            request,
            *args,
            **kwargs)


def mass_students_delete(request, objects=None):
    if request.method == 'GET':
            students_id = request.GET.getlist('checks')
            objects = Student.objects.filter(pk__in=students_id)
            return render(
                request,
                'students_confirm_delete.html',
                {'objects': objects, 'ids': students_id})
    else:
        students_id = request.POST.getlist('values')
        objects = Student.objects.filter(pk__in=students_id).delete()
        return HttpResponseRedirect(
            u'%s?status_message=Cтудентів було видалено.'
            % reverse('home'))
