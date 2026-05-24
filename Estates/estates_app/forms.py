from django import forms
from .models import *


class EstateForm(forms.ModelForm):
    class Meta:
        model = Estate
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EstateForm, self).__init__(*args, **kwargs)
        for field_name, field in list(self.fields.items()):
            if not isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-control'
