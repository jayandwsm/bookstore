from django.conf.urls import url
from booksInfo import views
urlpatterns = [
    url(r'^$',views.show_index,name="index"),
    url(r'^change_p/',views.change_password,name="change_p"),
    url(r'^detail/',views.show_detail,name="detail"),
    url(r'^search/',views.search_book,name="search"),
]