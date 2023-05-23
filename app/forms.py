from django import forms
from .models import Client


class NewClientForm(forms.ModelForm):

    class Meta:
        model = Client
        exclude = ["slug"]
        widgets = {
        }