from django.conf.urls import url
from userInfo import views
urlpatterns = [
    url(r'^regist/',views.regist,name="regist"),
    url(r'^regist_in/',views.regist_in,name="regist_in"),
    url(r'^verify_code/',views.verify_code,name="verify_code"),
    url(r'^login/',views.login,name="login"),
    url(r'^login_in/',views.login_in,name="login_in"),
    url(r'^logout/',views.logout,name="logout"),
    url(r'^checkname',views.check_name,name="checkname"),
    url(r'^person/',views.show_person,name="person"),
    url(r'^show_address/',views.show_address,name="show_address"),
    url(r'^add_address/',views.add_address,name="add_address"),
    url(r'^del_address/',views.del_address,name="del_address"),
    url(r'^change_address/',views.change_address,name="change_address"),
    url(r'^finish_order/',views.finish_order,name="finish_order"),
    url(r'^add/',views.add,name="add"),
    url(r'^save_book/',views.save_book,name="save_book"),
    url(r'^del_save/',views.del_save,name="del_save"),
    # url(r'^finish_order/',views.finish_order,name="finish_order"),

]