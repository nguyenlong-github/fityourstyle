from django.contrib import admin
from .models import CustomUser  
from .models import Appointment, Store, StoreHours
from django.contrib.auth.admin import UserAdmin


# Đăng ký CustomUser với admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('avatar', 'phone_number', 'date_of_birth')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('first_name', 'last_name', 'avatar', 'phone_number', 'date_of_birth')}),
    )

# Đăng ký model CustomUser với admin
admin.site.register(CustomUser, CustomUserAdmin)


# Đăng ký model Store với admin
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'id')  # Thêm thông tin cần hiển thị
    readonly_fields = ('id',)  # Trường id chỉ đọc


# Đăng ký model Appointment với admin
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'store', 'date', 'time', 'id')  # Thêm thông tin cần hiển thị
    readonly_fields = ('id',)  # Trường id chỉ đọc


# Đăng ký model StoreHours với admin
@admin.register(StoreHours)
class StoreHoursAdmin(admin.ModelAdmin):
    list_display = ('store', 'day_of_week', 'opening_time', 'closing_time')  # Thêm thông tin cần hiển thị
    list_filter = ('store', 'day_of_week')  # Lọc theo cửa hàng và ngày trong tuần
    search_fields = ('store__name',)  # Tìm kiếm theo tên cửa hàng
    ordering = ('store', 'day_of_week')  # Sắp xếp theo cửa hàng và ngày trong tuần
