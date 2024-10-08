"""vinsurvin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views as user_views
from product import views as product_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/new', user_views.create_user, name='create_user'),
    path('user/login', user_views.login, name='login'),
    path('user/info', user_views.get_user_info, name='get_user_info'),
    path('product/', product_views.get_products, name='get_products'),
    path('product/<int:numero>', product_views.get_product, name='get_product'),
    path('add-to-cart/', user_views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/', user_views.remove_from_cart, name='remove_from_cart'),
    path('get-cart/', user_views.get_cart, name='get_cart'),
    path('delete-cart/', user_views.delete_cart, name='delete_cart'),
    path('product/search/', product_views.search_product, name='search_product'),
    path('create-order/', user_views.create_order, name='create_order'),
    path('get-orders/', user_views.get_orders, name='get_orders'),
    path('mark-order-delivered/', user_views.mark_order_delivered, name='mark_order_delivered'),
    path('cancel-order/', user_views.cancel_order, name='cancel_order'),
]
