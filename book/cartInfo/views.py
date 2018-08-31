import json

import logging

import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from pymysql import DatabaseError

from booksInfo.models import Book
from cartInfo.models import Cart, Order
from userInfo.models import UserInfo, Address


def addcart(request):
    # 1.从session中获取用户id
    # 2.从前端页面获取书id和书数量
    # 3.得到2个对象，新建一个购物车类
    # 4.判断购物车中是否有这个商品有则累加
    # 无则添加数量
    # 5.保存数据库向前端页面返回一个success
    userid = request.session["id"]
    bookid = request.POST.get("bookid")
    ccount = request.POST.get("bookunit")
    old_user = UserInfo.objects.get(id=userid)
    # print(old_user)
    old_book = Book.objects.get(id=bookid)
    # print(old_book[0])
    new_cart = Cart()
    # print(new_cart)
    check_cart = Cart.objects.filter(user_id=userid,book_id=bookid)

    if not userid:
        return redirect("/userinfo/login")
    else:
        if not bookid:
            return HttpResponse(json.dumps({"message":"error"}))
        else:
            # if len(check_user) > 0:
            #     check_user[0].user = old_user
            #     if len(check_book) > 0:
            #         check_user[0].book = old_book
            #         check_user[0].ccount = int(ccount) + check_user[0].ccount
            #     else:
            #         check_user[0].book = old_book
            #         check_user[0].ccount = int(ccount)
            #         try:
            #             check_user[0].save()
            #         except DatabaseError as e:
            #             logging.warning(e)
            #         return render(request, "detail.html", json.dumps({"message": "success"}))
            # else:
            #     new_cart.user = old_user
            #     new_cart.book = old_book
            #     new_cart.ccount = int(ccount)
            # try:
            #     new_cart.save()
            # except DatabaseError as e:
            #
            # logging.warning(e)
            # return render(request, "detail.html", json.dumps({"message":"success"}))
            try:
                if len(check_cart) <= 0:
                    new_cart.user = old_user
                    new_cart.book = old_book
                    new_cart.ccount = int(ccount)
                    new_cart.save()
                else:
                    check_cart[0].ccount = check_cart[0].ccount + int(ccount)
                    check_cart[0].save()
            except DatabaseError as e:
                logging.warning(e)
            return HttpResponse(json.dumps({"message": "success"}))

    # return render(request, "detail.html")
def show_cart(request):
    sess_id = request.session.get("id")
    if not sess_id:
        return redirect("/userinfo/login")
    else:
        userid = sess_id
        try:
            carts = Cart.objects.filter(user_id=userid)
        except DatabaseError as e:
            logging.warning(e)
        return render(request,"cart.html",locals())


def del_book(request):
    # 1.获取前端页面传来的bookid
    # 2.得到cart对象删除book
    # 3.返回删除成功信息到前端
    # 4.前端重新加载页面
    bookid = request.GET.get("bookid")
    # print(bookid)
    del_cart = Cart.objects.filter(book_id=bookid)
    try:
        a = del_cart[0].delete()
    except DatabaseError as e:
        logging.warning(e)
    return HttpResponse(json.dumps({"message":"ok"}))

def order(request):
    userid = request.session["id"]
    address = Address.objects.filter(user_id=userid)
    return render(request,"order.html",locals())

def corder(request):
    # 1.从session中获取用户
    # 2.从前端页面获取订单表的全部信息保存进订单表
    # 3.返回到前端成功
    # ordernum = models.CharField("订单号", max_length=50)
    # orderdetail = models.TextField("订单详情")
    # addressname = models.CharField("收件人", max_length=50)
    # addressphone = models.CharField("收件人电话", max_length=20)
    # orderaddress = models.CharField("收件人地址", max_length=100)
    # ordertime = models.DateField(auto_now=True)
    # orderacot = models.IntegerField("总数")
    # orderacount = models.DecimalField("总价", max_digits=8, decimal_places=2)
    # orderstatus = models.IntegerField("状态", choices=ORDERCHOICES, default=1)
    # user = mode
    # "adsname":$('input:radio:checked').attr('_addname'),
    # "adsphone":$('input:radio:checked').attr('_addphone'),
    # "adsaddress":$('input:radio:checked').attr('_add'),
    # "acot":$("#num").attr("_acot"),
    # 'orderacount':$("#num").attr("_count"),
    # "detail": sessionStorage.getItem('acot')},
    userid = request.session["id"]
    old_user = UserInfo.objects.filter(id=userid)
    new_order = Order()
    new_order.ordernum = datetime.datetime.now().strftime("%y%m%d%h%m%s")
    new_order.orderdetail = request.POST.get("detail")
    new_order.addressname = request.POST.get("adsname")
    new_order.addressphone = request.POST.get("adsphone")
    new_order.orderaddress = request.POST.get("adsaddress")
    new_order.orderacot = request.POST.get("acot")
    new_order.orderacount = request.POST.get("orderacount")
    new_order.user = old_user[0]
    try:
        new_order.save()
    except DatabaseError as e:
        logging.warning(e)
    return HttpResponse(json.dumps({"message":"ok"}))

