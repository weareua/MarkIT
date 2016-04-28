from django.forms import ModelForm
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from students.models import Student

class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'birthday',
            'photo',
            'ticket',
            'student_group',
            'notes'
            ]

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse(
            'students_edit',
            kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_show_labels = True
        # self.helper.render_unmentioned_fields = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        self.helper.add_input(Submit('submit', 'Зберегти'))
        self.helper.add_input(Submit(
            'cancel_button',
            'Скасувати',
            css_class="btn btn-link"))

