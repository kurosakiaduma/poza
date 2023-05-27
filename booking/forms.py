from django.forms import *
from .models import Appointment

from django.db import models
# Create the form class.

class CompletedForm(ModelForm):
    completed = BooleanField()
    class Meta:
        model = Appointment
        fields = ['completed']
        db_table = 'booking_appointment'
        managed = True
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'