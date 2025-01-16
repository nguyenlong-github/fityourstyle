from django.contrib import admin
from .models import Appointment, User, Store, StoreHours
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'first_name', 'last_name','id')
    readonly_fields = ('id',)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner','id')
    readonly_fields = ('id',) 


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'store', 'date', 'time','id')    
    readonly_fields = ('id',)

@admin.register(StoreHours)
class StoreHoursAdmin(admin.ModelAdmin):
    list_display = ('store', 'day_of_week', 'opening_time', 'closing_time')
    list_filter = ('store', 'day_of_week')  # Lọc theo cửa hàng và ngày trong tuần
    search_fields = ('store__name',)        # Tìm kiếm theo tên cửa hàng
    ordering = ('store', 'day_of_week')     # Sắp xếp theo cửa hàng và ngày trong tuần

