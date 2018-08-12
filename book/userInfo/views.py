import json
import logging
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from pymysql import DatabaseError
from requests import session

from cartInfo.models import Order
from userInfo.models import UserInfo, Address


def regist(request):
    return render(request, "regist_login.html")

def check_name(request):
    username = request.POST.get("username")
    print(username)
    check_user = UserInfo.objects.filter(username=username)
    if len(check_user) >= 1:
        content={"error":"fail"}
        return HttpResponse(json.dumps(content))
        # return render(request,'regist_login.html',{"error":"用户名已存在"})
    else:
        return HttpResponse(json.dumps({"success":"suc"}))
def regist_in(request):
    # 1.判断是否为post是获取前端页面传来的信息否返回注册页面
    # 2.创建新的用户类
    # 3.判断用户名是否存在,存在返回用户名已经存在
    # 4.判断是否有空
    # 5.对密码进行加密处理
    # 6.保存进数据库
    # 7.异常处理
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        new_user = UserInfo()
        username_exist = UserInfo.objects.filter(username=username)
        if len(username_exist) == 1:
            return render(request, "regist_login.html",{"error":"用户名已经存在"})
        else:
            if password and email and phone:
                f_password = make_password(password,"a","pbkdf2_sha256")
                new_user.username = username
                new_user.password = f_password
                new_user.email = email
                new_user.phone = phone
                try:
                    new_user.save()
                except DatabaseError as e:
                    logging.warning(e)
                return redirect("/")
            else:
                return render(request, "regist_login.html", {"error": "请填写全部信息"})
    else:
        return redirect("/userinfo/regist")


def login(request):
    return render(request, "regist_login.html")

def login_in(request):
    # 1.判断是否为post否重定向登录页面
    # 2.从前端页面获得用户名密码
    # 3.判断用户名是否存在,存在判断密码是否正确是则在session中存储用户id和用户名并进入index，
    # 否重定向到登录也并显示错误信息
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print(username)
        username_exist = UserInfo.objects.filter(username=username)
        print(username_exist)
        # print(username_exist[0].username)
        # print(username_exist[0].password)
        if len(username_exist) <1:
            return render(request, "regist_login.html", {"message": "用户名或密码错误"})
        if check_password(password,username_exist[0].password):
            request.session["id"] = username_exist[0].id
            request.session["username"] = username_exist[0].username
            return redirect("/")
        else:
            return render(request, "regist_login.html", {"message": "用户名或密码错误"})
    else:
        return redirect("/userinfo/login")

def logout(request):
    try:
        if request.session["username"] :
            del request.session["username"]
            del request.session["id"]
    except DatabaseError as e:
        logging.warning(e)
    return redirect('/')

def show_address(request):
    userid = request.session["id"]
    address = UserInfo.objects.get(id=userid).add.all()
    # address = Address.objects.filter(user_id=userid)
    # print(address)
    return render(request,"address.html",locals())

def show_person(request):
    username = request.session.get("username")
    if not username:
        return redirect("/userinfo/login")
    else:
        try:
            old_user = UserInfo.objects.filter(username=username)
            return render(request,"person.html",{"old_user":old_user[0]})
        except DatabaseError as e:
            logging.warning(e)

def add_address(request):
    new_address = Address()
    userid = request.session["id"]
    addressname = request.POST.get("addressname")
    address = request.POST.get("address")
    addressphone = request.POST.get("addressphone")
    print(address)
    if addressname and address and addressphone:
        user = UserInfo.objects.get(id=userid)
        new_address.adname = addressname
        new_address.address = address
        new_address.adphone = addressphone
        new_address.user = user
        try:
            new_address.save()
        except DatabaseError as e:
            logging.warning(e)
    else:
        return redirect("/userinfo/show_address/")
    return redirect("/userinfo/show_address/")

def del_address(request):
    addid = request.GET.get("delid")
    a = Address.objects.get(id=addid).delete()
    return HttpResponse(json.dumps({"static":"ok"}))

def change_address(request):
    addressname = request.POST.get("name")
    address = request.POST.get("address")
    addressphone = request.POST.get("phone")
    addressid = request.POST.get("addressid")
    old_address = Address.objects.get(id=addressid)
    old_address.adname = addressname
    old_address.address = address
    old_address.adphone = addressphone
    try:
        old_address.save()
    except DatabaseError as e:
        logging.warning(e)
    return HttpResponse(json.dumps({"static":"ok"}))

def finish_order(request):
    userid = request.session["id"]
    old_order = Order.objects.filter(user_id=userid)
    print()
    return render(request,"finish_order.html",locals())
