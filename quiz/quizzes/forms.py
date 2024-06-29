from django import forms
from .models import Quiz


class QuizForm(forms.ModelForm):
    # This form allows you to define which fields of the Quiz template will be included in each form
    # You can manage multiple separate forms on a single page,
    # by including a hidden field that identifies the form submitted.
    edit_quiz = forms.BooleanField(widget=forms.HiddenInput, initial=True)  # attached an edit_quiz field
    
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'category']  # inclure les champs nécessaires


class DeleteQuizForm(forms.Form):
    # You can manage multiple separate forms on a single page,
    # by including a hidden field that identifies the form submitted.
    delete_quiz = forms.BooleanField(widget=forms.HiddenInput, initial=True)  # attached an delete_quiz field
