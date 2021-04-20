from django.forms import ModelForm, TextInput, CharField
from .models import Environ
from main.models import Task, File
from tinymce.widgets import TinyMCE
from django import forms

class EnvForm(ModelForm):
    # name = CharField(widget = TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Environ
        fields = ['name']

class TaskForm(ModelForm):
    desc = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    # name = CharField(widget = TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Task
        fields = ['title', 'type', 'hard', 'project', 'desc', 'budget']

class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['title', 'image', 'task']
        widgets = {'task': forms.HiddenInput()}