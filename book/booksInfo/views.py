import json
import logging

from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.decorators.cache import cache_page
from pymysql import DatabaseError

from booksInfo.models import BookType, Book
from cartInfo.models import Cart
from userInfo.models import UserInfo

def show_index(request):
    # print('hahhah')
    # 1.查询全部分类
    # 2.查询对应分类的商品展示在页面
    try:
        # book_list = []
        # all_type = BookType.objects.all()
        # print(all_type)
        # for type in all_type:
            # print(type)
        # b = {}
        # b["type"] = type
        # book_type = get_object_or_404(BookType,typename=type.typename)
        # all_books = list(book_type.book_set.all())
        # b["book"] = all_books
        # book_list.append(b)
        #
        # print(book_list)

        # print(new_book_type)
        all_books = Book.objects.all()
        # print(all_books)
    except DatabaseError as e:
        logging.warning(e)
    return render(request,"index.html",locals())

def change_password(request):
    # 1.从网页获取旧密码
    # 2.从session中获取用户并查询返回对象
    # 3.判断密码是否正确,正确修改数据库并返回修改成功
    # 4.错误返回密码有误
    old_password = request.POST.get("old_password")
    new_password = request.POST.get("new_password")
    # print(old_password)
    username = request.session["username"]
    old_user = UserInfo.objects.get(username = username)
    if check_password(old_password,old_user.password):
        old_user.password = make_password(new_password,"a","pbkdf2_sha256")
        try:
            old_user.save()
        except DatabaseError as e:
            logging.warning(e)
        return HttpResponse(json.dumps({"success":"success"}))
    else:
        # return render(request,"person.html",{"message":"密码有误"})
        return HttpResponse(json.dumps({"fail":"fail"}))

def show_detail(request):
    # 1.点击链接发送商品id到后端
    # 2.获取商品id
    # 3.在数据库查询商品返回给book.html
    bookid = request.GET.get("bookid")
    # print(bookid)
    d_book = Book.objects.get(id=bookid)
    return render(request,"detail.html",locals())





