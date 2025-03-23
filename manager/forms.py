from django import forms
from django.contrib.auth import get_user_model
from django.forms import DateInput

from manager.models import Task, Team


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )
    deadline = forms.DateField(
        widget=DateInput(attrs={"type": "date", "placeholder": "DD/MM/YYYY"}, format="%d/%m/%Y")
    )

    class Meta:
        model = Task
        fields = '__all__'
