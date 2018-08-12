from django.conf.urls import url
from cartInfo import views

urlpatterns = [
    url(r'^addcart/',views.addcart,name="addcart"),
    url(r'^cart/',views.show_cart,name="cart"),
    url(r'^delbook/',views.del_book,name="delbook"),
    url(r'^order/',views.order,name="order"),
    url(r'^corder/',views.corder,name="corder"),
]