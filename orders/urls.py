from django import urls
from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth import logout
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    url(r'^logout/', views.logout, name="logout"),
    
    re_path(r'^cart/add/(?P<nombre_producto>.*)/(?P<p_precio>.*)/$', views.cart_add, name='cart_add'),
    path("cart/add/pizza/", views.cart_add_pizza, name="cart_add_pizza"),
    path('update/(?P<id_cart>.*)/', views.confirmar, name="confirmar"),
    path('delete/(?P<id_cart>.*)/', views.borrar, name="borrar"),
    path('ordenes/', views.ordenes, name="ordenes"),
    path('historial/', views.historial, name="historial"),
    path('Admin/', views.Admin, name="Admin" ),
    path('conf_envi/(?P<confirmar_id>.*)/', views.conf_envi, name="conf_envi"),
    path('borrar_pedido/(?P<confirmar_id>.*)/', views.borrar_pedido, name="borrar_pedido")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)