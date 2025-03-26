from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.forms import DateInput

from manager.models import Task, Team, Project, Worker


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
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        required=False
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
        queryset=Project.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        required=False
    )

    class Meta:
        model = Team
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['members'].initial = self.instance.members.all()
            self.fields['projects'].initial = self.instance.projects_team.all()


class WorkerForm(UserChangeForm):
    password = None

    class Meta:
        model = Worker
        fields = (
            "username",
            "first_name",
            "last_name",
            "position",
            "email",
            "team"
        )


class TaskNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Search... (name)",
            "class": "form-control",
            "style": "width: 300px;"
        }),
        label=""
    )
