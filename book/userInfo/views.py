import json
import logging
import random
import string
import io
import random

from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.views.decorators.cache import cache_page
from pymysql import DatabaseError
from requests import session

from booksInfo.models import Book
from cartInfo.models import Order
from userInfo.models import UserInfo, Address, Save


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

# 生成验证码
def verify_code(request):
    #引入随机函数模块

    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = string.digits+string.ascii_uppercase+string.ascii_lowercase
    #随机选取4个值作为验证码
    code = ''
    for i in range(0, 4):
        code += random.choice(str1)
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), code[0], font=font, fill=fontcolor)
    draw.text((25, 2), code[1], font=font, fill=fontcolor)
    draw.text((50, 2), code[2], font=font, fill=fontcolor)
    draw.text((75, 2), code[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['code'] = code
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的

    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

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
        codeN = request.POST.get("codeN")
        # print(codeN)
        code = request.session.get("code")
        # print(code)
        # print(username)
        username_exist = UserInfo.objects.filter(username=username)
        # print(username_exist)
        # print(username_exist[0].username)
        # print(username_exist[0].password)
        if codeN.lower() != code.lower():
            return render(request, "regist_login.html", {"message": "验证码错误"})
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
        check_user = request.session.get("username")
        print(check_user)
        if check_user:
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
    # print(address)
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

def add(request):
    # 1.session可以获取用户
    # 2.前端可以获取书
    # 3.判断这个人是否有这本书，没有添加，有返回
    # if not
    # 1.获取前端传来的id
    bookid = request.GET.get("bookid")
    # 3.从session中获取用户id
    # print(bookid)
    userid = request.session.get("id")
    if not userid:
        return redirect("/userinfo/login")
    else:
    # 2.通过id查询商品
        user = UserInfo.objects.get(id=userid)
        book = Book.objects.get(id=bookid)
        # 4.保存进数据库
        #判断数据库这个人是否有这本书
        s = Save.objects.filter(user_id=userid,book_id=bookid)
        new_save = Save()
        # check_book = s[0].objects.filter(book_id=bookid)
        if len(s)>0:
            return HttpResponse(json.dumps({"success": "again"}))
        new_save.user = user
        new_save.book = book
        try:
            new_save.save()
        except DatabaseError as e:
            logging.warning(e)
        # 5.返回给ajax
        return HttpResponse(json.dumps({"success":"suc"}))

def save_book(request):
    # 1.获取用户session中的id
    userid = request.session.get("id")
    save = Save.objects.filter(user_id=userid)
    # 2.通过userid获取用户所有的书
    #3.返回save页面
    return render(request,"save.html",locals())

@cache_page(30)
def finish_order(request):
    # print("hahahah")
    userid = request.session["id"]
    old_order = Order.objects.filter(user_id=userid)
    return render(request,"finish_order.html",locals())
