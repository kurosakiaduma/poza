from django.contrib import admin
from .models import *
from chat.models import Chat

admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Chat)