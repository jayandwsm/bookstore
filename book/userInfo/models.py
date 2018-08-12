from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField('用户名',max_length=50,null=False)
    password = models.CharField('密码',max_length=200,null=False)
    phone = models.CharField('电话',max_length=20,null=False)
    email = models.CharField('邮箱',max_length=50,null=False)
    time = models.DateField('注册时间',auto_now=True)
    isban = models.BooleanField('是否禁用',default=False)
    isdelete = models.BooleanField('是否删除',default=False)

    def __str__(self):
        return self.username

class Address(models.Model):
    address = models.CharField("收获地址",max_length=100,null=False)
    adphone = models.CharField("收件电话",max_length=20,null=False)
    adname = models.CharField("收件人",max_length=50,null=False)
    user = models.ForeignKey(UserInfo,related_name="add",on_delete=models.CASCADE)

    def __str__(self):
        return self.address