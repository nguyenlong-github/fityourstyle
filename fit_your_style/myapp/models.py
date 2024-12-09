from django.db import models

class Appointment(models.Model):
    surname = models.CharField(max_length=30, verbose_name='姓')
    name = models.CharField(max_length=30,verbose_name='名')
    email = models.EmailField(verbose_name='メールアドレス')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='電話番号')
    date = models.DateField(verbose_name='日付')
    time = models.TimeField(verbose_name='時刻')
    status = models.CharField(max_length=10,verbose_name='ステータス',default='pending')
    message = models.TextField(max_length=500, null=True,blank=True,verbose_name='メッセージ')
    picture = models.ImageField(upload_to='myapp/picture', blank=True,null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="作成時間")
    update_at = models.DateTimeField(auto_now_add=True, verbose_name="変更時間")
    def __str__(self):
        return f"{self.name} {self.surname}"