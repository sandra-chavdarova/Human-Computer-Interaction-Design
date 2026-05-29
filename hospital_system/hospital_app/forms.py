from django import forms

# Define your forms here.

from .models import *


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ("appointment_type", "responsible_doctor")

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
