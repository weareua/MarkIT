# -*- coding: utf-8 -*-

import logging

from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from MarkIT.settings import ADMIN_EMAIL
from exams.forms import ExamForm


class ContactForm(forms.Form):

    subject = forms.CharField(
        label=u"Заголовок листа",
        max_length=128)

    from_email = forms.EmailField(
        label=u"Ваша поштова скринька")

    message = forms.CharField(
        label=u"Текст повідомлення",
        max_length=2560,
        widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        # self.helper.form_action = reverse_lazy('home')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        # self.helper.help_text_inline = False
        self.helper.html5_required = False
        self.helper.form_show_labels = True
        self.helper.render_unmentioned_fields = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        self.helper.add_input(Submit('submit', 'Відіслати'))
        self.helper.add_input(Submit(
            'cancel_button',
            'Скасувати',
            css_class="btn btn-link"))


class ContactView(FormView):
    template_name = 'contact/form.html'
    form_class = ExamForm
    success_message = u'Повідомлення успішно відправлено.'
    success_url = reverse_lazy('home')

    @method_decorator(permission_required('auth.add_user'))
    def dispatch(self, *args, **kwargs):
        return super(ContactView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):

            messages.error(request, u'Заповнення форми було скасоване')
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return super(ContactView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        """This method is called for valid data"""
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        from_email = form.cleaned_data['from_email']
        try:
            send_mail(
                subject,
                message+'\n\nMessage was send from: '+from_email,
                'Students DB ',
                [ADMIN_EMAIL])
        except Exception:
                message = u'Під час відправки листа виникла непередбачувана ' \
                    u'помилка. Спробуйте скористатись даною формою пізніше.'
                logger = logging.getLogger(__name__)
                logger.exception(message)

                messages.add_message(
                    self.request,
                    messages.ERROR,
                    u'Під час відправки листа виникла непередбачувана ' \
                    u'помилка. Спробуйте скористатись даною формою пізніше.'
                    )
        else:
            storage = messages.get_messages(self.request)
            messages.add_message(
                self.request,
                messages.INFO,
                u'Повідомлення успішно надіслано.')
        return super(ContactView, self).form_valid(form)
