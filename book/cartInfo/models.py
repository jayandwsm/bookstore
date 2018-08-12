from django.db import models

# Create your models here.
from booksInfo.models import Book
from userInfo.models import UserInfo

ORDERCHOICES = (
    (1,"未支付"),
    (2,"已支付"),
    (3,"取消订单"),
)

class Cart(models.Model):
    user = models.ForeignKey(UserInfo,db_column="user_id",on_delete=models.CASCADE)
    book = models.ForeignKey(Book,db_column="book_id",on_delete=models.CASCADE)
    ccount = models.IntegerField("数量",db_column="book_count")

    def __str__(self):
        return self.user.username

class Order(models.Model):
    ordernum = models.CharField("订单号",max_length=50)
    orderdetail = models.TextField("订单详情")
    addressname = models.CharField("收件人",max_length=50)
    addressphone = models.CharField("收件人电话",max_length=20)
    orderaddress = models.CharField("收件人地址",max_length=100)
    ordertime = models.DateField(auto_now=True)
    orderacot = models.IntegerField("总数")
    orderacount = models.DecimalField("总价",max_digits=8,decimal_places=2)
    orderstatus = models.IntegerField("状态",choices=ORDERCHOICES,default=1)
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)

    def __str__(self):
        return self.ordernum




