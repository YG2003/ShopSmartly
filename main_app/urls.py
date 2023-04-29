from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',register, name="register"),
    path('login/',views.LoginView.as_view(template_name="main_app/login.html"), name="login"),
    path('logout/',views.LogoutView.as_view(template_name="main_app/logout.html"), name="logout"),
    path('', home,name="home"),
    path('index', index, name = "index"),
    path('amazon', AmazonItem,name="amazon"),
    path('delete_item/<int:pk>', delete_item_amazon,name="delete-item-amazon"),
    path('flipkart', FlipkartItem,name="flipkart"),
    path('delete_item/<int:pk>', delete_item_flipkart,name="delete-item-flipkart"),
    path('view_all', view_all,name="view-all"),
    path('delete_item/<int:pk>', delete_item,name="delete-item"),

    
]
