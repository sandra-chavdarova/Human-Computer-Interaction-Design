from django import forms
from .models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ("image",)

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
