from django import forms
from django.contrib.auth import get_user_model
from django.forms import DateInput

from manager.models import Task, Team, Project


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )
    deadline = forms.DateField(
        widget=DateInput(attrs={"type": "date", "placeholder": "DD/MM/YYYY"})
    )

    class Meta:
        model = Task
        fields = '__all__'


class ProjectForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = Project
        fields = "__all__"


class TeamForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )

    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = Team
        fields = "__all__"