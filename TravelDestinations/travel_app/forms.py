from django import forms
from .models import *


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Travel
        exclude = ("guide",)

    def __init__(self, *args, **kwargs):
        super(DestinationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
