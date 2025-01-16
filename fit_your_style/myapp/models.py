import uuid
from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='USER_ID')
    first_name = models.CharField(max_length=50, verbose_name='名')
    last_name = models.CharField(max_length=50, verbose_name='姓')
    user_name = models.CharField(max_length=50, verbose_name='ユーザー名')
    password = models.CharField(max_length=50, verbose_name='パスワード')
    email = models.EmailField(unique=True, verbose_name='メールアドレス')
    avatar = models.ImageField(upload_to='picture/user_avatar', blank=True, null=True, verbose_name='アバター')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='電話番号')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='生年月日')
    created_at = models.DateTimeField(auto_now=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  

class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='STORE_ID')
    name = models.CharField(max_length=100, verbose_name='店名')
    owner = models.CharField(max_length=15, blank=True, null=True, verbose_name='店長')
    address = models.TextField(verbose_name='住所')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='電話番号')
    email = models.EmailField(blank=True, null=True, verbose_name='メールアドレス')
    created_at = models.DateTimeField(auto_now=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        return self.name

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='APPOINTMENT_ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', verbose_name='ユーザー')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='appointments', verbose_name='店名')
    picture = models.ImageField(upload_to='picture/user_appointment', blank=True, null=True, verbose_name='写真')
    date = models.DateField(verbose_name='日付')
    time = models.TimeField(verbose_name='時刻')
    message = models.TextField(blank=True, null=True, verbose_name='備考')
    created_at = models.DateTimeField(auto_now=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        return f"Appointment for {self.user} at {self.store} on {self.date} {self.time}"
