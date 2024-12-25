from django.contrib import admin

from .models import Appointment, User

# Register your models here.

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "time",)
admin.site.register(Appointment,AppointmentAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name")
admin.site.register(User,UserAdmin)