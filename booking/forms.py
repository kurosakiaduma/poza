from django.forms import ModelForm
from .models import Appointment
from tkinter import Widget
from django.db import models
# Create the form class.
class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ["service", "day", "time", "time_ordered"]
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['service'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['day'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['time'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['time_ordered'].widget.attrs['class'] = 'form-control form-control-lg'
        