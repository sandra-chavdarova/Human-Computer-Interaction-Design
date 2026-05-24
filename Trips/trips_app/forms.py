from django.forms import ModelForm
from .models import Trip


class TripForm(ModelForm):
    class Meta:
        model = Trip
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'