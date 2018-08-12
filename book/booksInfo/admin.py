from django.contrib import admin

# Register your models here.
from booksInfo.models import *
admin.site.register(Book)
admin.site.register(BookType)