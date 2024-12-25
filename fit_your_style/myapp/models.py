from django.db import models
import uuid
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_name = models.CharField(max_length=30, verbose_name='名前')
    first_name = models.CharField(max_length=30, verbose_name='姓')
    email = models.EmailField(max_length=254, verbose_name='メールアドレス')
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name='住所')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='電話番号')
    avatar = models.ImageField(upload_to='myapp/avatar', null=True, blank=True)
    password = models.CharField(max_length=30, verbose_name='パスワード')
    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(verbose_name='日付')
    time = models.TimeField(verbose_name='時刻')
    status = models.CharField(max_length=10,verbose_name='ステータス',default='pending')
    message = models.TextField(max_length=500, null=True,blank=True,verbose_name='メッセージ')
    picture = models.ImageField(upload_to='myapp/picture', blank=True,null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="作成時間")
    update_at = models.DateTimeField(auto_now_add=True, verbose_name="変更時間")
    def __str__(self):
        return f"{self.id} {self.date} {self.time}"