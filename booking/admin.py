from django.contrib import admin
from .models import *
from chat.models import Chat


admin.site.register(Appointment)
admin.site.register(Chat)
@admin.register(Persona)
class UserAdmin(admin.ModelAdmin):
    pass