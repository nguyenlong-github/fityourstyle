from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Tạo CustomUser kế thừa từ AbstractUser
class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='myapp/picture/user_avatar', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


# Model Store
class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='STORE_ID')
    name = models.CharField(max_length=100, verbose_name='店名')  # Store name
    owner = models.CharField(max_length=15, blank=True, null=True, verbose_name='店長')  # Store owner name
    address = models.TextField(verbose_name='住所')  # Store address
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='電話番号')  # Store phone number
    email = models.EmailField(blank=True, null=True, verbose_name='メールアドレス')  # Store email
    created_at = models.DateTimeField(auto_now=True, verbose_name="作成日時")  # Created date
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")  # Updated date

    def __str__(self):
        return self.name


# Model Appointment
class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='APPOINTMENT_ID')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments', verbose_name='ユーザー')  # Thay User bằng CustomUser
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='appointments', verbose_name='店名')
    picture = models.ImageField(upload_to='myapp/picture/user_appointment', blank=True, null=True, verbose_name='写真')  # Appointment picture
    date = models.DateField(verbose_name='日付')  # Appointment date
    time = models.TimeField(verbose_name='時刻')  # Appointment time
    message = models.TextField(blank=True, null=True, verbose_name='備考')  # Appointment message
    created_at = models.DateTimeField(auto_now=True, verbose_name="作成日時")  # Created date
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")  # Updated date

    def __str__(self):
        return f"Appointment for {self.user} at {self.store} on {self.date} {self.time}"


# Model StoreHours
class StoreHours(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_hours', verbose_name='店名')
    day_of_week = models.IntegerField(choices=[  # Store hours for each day of the week
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
        (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')],
        verbose_name='曜日'
    )
    opening_time = models.TimeField(verbose_name='開始時間')  # Opening time
    closing_time = models.TimeField(verbose_name='終了時間')  # Closing time

    def __str__(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return f"{self.store.name} - {days[self.day_of_week]}"
