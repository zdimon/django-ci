from django.forms import ModelForm, TextInput, CharField
from .models import Environ


class EnvForm(ModelForm):
    # name = CharField(widget = TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Environ
        fields = ['name']
