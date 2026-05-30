from django import forms
from .models import Cake


class CakeForm(forms.ModelForm):
    class Meta:
        model = Cake
        exclude = ("baker",)

    def __init__(self, *args, **kwargs):
        super(CakeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
