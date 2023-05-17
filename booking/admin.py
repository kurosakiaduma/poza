from django.contrib import admin
from .models import *
from chat.models import Chat
from ajax_select import make_ajax_form

admin.site.register(Chat)
@admin.register(Persona)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    
    form = make_ajax_form(Appointment, {
        
    })