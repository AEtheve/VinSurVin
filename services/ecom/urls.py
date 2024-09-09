"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
    path("admin/", admin.site.urls),
    path("user/", user_views.index),
    path("user/add/", user_views.add_user),
    path("user/get/", user_views.get_user),
    path("product/add/", product_views.add_product),
    path("product/", product_views.get_product),
    path('product/<int:product_id>/', product_views.get_product_by_id),
]