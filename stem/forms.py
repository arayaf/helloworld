from django import forms
from .models import StudyGroup, Quiz, QuizOption


class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['name', 'description', 'subject', 'is_public', 'max_members']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'max_members': forms.NumberInput(attrs={'min': 2, 'max': 50}),
        }


class QuizSubmissionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        quiz = kwargs.pop('quiz', None)
        super().__init__(*args, **kwargs)
        
        if quiz:
            if quiz.question_type == 'multiple_choice':
                options = quiz.options.all()
                self.fields['selected_option'] = forms.ModelChoiceField(
                    queryset=options,
                    widget=forms.RadioSelect,
                    empty_label=None,
                    required=True
                )
            elif quiz.question_type == 'true_false':
                options = quiz.options.all()
                self.fields['selected_option'] = forms.ModelChoiceField(
                    queryset=options,
                    widget=forms.RadioSelect,
                    empty_label=None,
                    required=True
                )
            elif quiz.question_type in ['fill_blank', 'short_answer']:
                self.fields['answer_text'] = forms.CharField(
                    widget=forms.Textarea(attrs={'rows': 3}),
                    required=True
                )