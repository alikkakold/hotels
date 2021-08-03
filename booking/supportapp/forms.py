from django import forms

from supportapp.models import Problem


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('problem', 'page')
