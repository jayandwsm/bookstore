from django.contrib import admin

# Register your models here.
from userInfo.models import *
admin.site.register(UserInfo)
admin.site.register(Address)