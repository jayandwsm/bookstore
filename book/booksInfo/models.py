from django.db import models

# Create your models here.
class BookType(models.Model):
    typename = models.CharField("分类名",max_length=50,null=False)
    typedesc = models.CharField("描述",max_length=100,default="类型描述")
    isdelete = models.BooleanField("删除",default=False)

    def __str__(self):
        return self.typename

class Book(models.Model):
    bookname = models.CharField("书名",max_length=50,null=False)
    bookprice = models.DecimalField(max_digits=8,decimal_places=2)
    bookdetail = models.CharField("图书细节",max_length=100,null=False)
    bookdesc = models.CharField("图书描述",max_length=200,null=False)
    bookpicture = models.ImageField("实物",upload_to="static/images/books",default="1.jpg")
    bookunit = models.CharField("单位",max_length=30,null=False)
    isdelete = models.BooleanField("删除",default=False)
    book = models.ForeignKey(BookType,on_delete=models.CASCADE)

    def __str__(self):
        return self.bookname

    def get_url(self):
        return "/detail/?bookid={}".format(self.id)