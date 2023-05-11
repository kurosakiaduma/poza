from django.contrib import admin
from .models import *
admin.site.register(Appointment)
admin.site.admin_view(Appointment)