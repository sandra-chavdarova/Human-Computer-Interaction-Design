from django import forms
from .models import *


class ExhibitionForm(forms.ModelForm):
    class Meta:
        model = Exhibition
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ExhibitionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
