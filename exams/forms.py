from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from exams.models import Exam



class ExamForm(ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        # self.helper.help_text_inline = False
        self.helper.html5_required = False
        self.helper.form_show_labels = True
        self.helper.render_unmentioned_fields = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        self.helper.add_input(Submit('submit', 'Зберегти'))
        self.helper.add_input(Submit(
            'cancel_button',
            'Скасувати',
            css_class="btn btn-link"))

