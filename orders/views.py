from django import forms
from django import contrib
from django.http import HttpResponseRedirect, HttpResponse, request
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.urls import reverse
from django.contrib.auth import logout as core_logout, login as auth_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
#from django.contrib.messages import constants as messages

# Create your views here.
def index(request):
    Regular = Product.objects.all().filter(TipoPizza__TipoPizza__icontains="Regular",Categoria__Categoria__icontains="Pizza")
    Sicilian = Product.objects.all().filter(TipoPizza__TipoPizza__icontains="Sicilian", Categoria__Categoria__icontains="Pizza")
    pasta = Product.objects.all().filter(Categoria__Categoria__icontains="Pasta")
    Ensalada = Product.objects.all().filter(Categoria__Categoria__icontains="Ensaladas")
    subs= Product.objects.all().filter(Categoria__Categoria__icontains="Subs")
    Dinner= Product.objects.all().filter(Categoria__Categoria__icontains="Bandejas de cena")
    Fritanga= Product.objects.all().filter(Categoria__Categoria__icontains="Fritanga")
    topping = Topping.objects.all()
    extra = Extra.objects.all()

    return render(request, "index.html", {"Regular": Regular, "Sicilian":Sicilian ,"pasta":pasta, "Subs":subs, "Ensalada":Ensalada, "Dinner":Dinner, "Topping":topping, 'Extra':extra, 'Fritanga':Fritanga})

# registro del usuario
def register(response):
    form = UserCreationForm()
    if response.method == 'POST':
        form = UserCreationForm(response.POST)
        print(form)
        if form.is_valid():
            form.save()
            #user = form.cleaned_data.get('username')
            #messages.success(response, 'Cuenta creada' + user)
            return redirect('index')
    return  render(response, 'register.html', {'form':form})

# Login de usuario
def login(request):
    if request.method == 'POST':
        
        form = AuthenticationForm(data=request.POST)
        print(form)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})

# Logout para el usuario
def logout(request):

    if request.method == 'POST':
        core_logout(request)
        return redirect('index')

@login_required(login_url="/login")
def cart_add(request,nombre_producto, p_precio):
    print("funciona?")
    user=request.user
    ordenes = CartItems(
        username=user,
        nombre = nombre_producto,
        precio=p_precio,
    )
    ordenes.save()
    print(ordenes, user)
    #cart = Cart(request)
    return redirect("index")


def confirmar(request, id_cart):
    ordenes = CartItems.objects.get(pk=id_cart)
    ordenes.estado = "True"
    ordenes.save()
    return redirect('ordenes')

def borrar(request, id_cart):
    ordenes = CartItems.objects.get(pk=id_cart)
    ordenes.delete()
    return redirect('ordenes')
@login_required(login_url="/login")
def cart_add_pizza(request):
    if request.method == 'POST':
        
        user=request.user
        nombre = request.POST.get("name")
        remplazo = request.POST.get("precio")
        lista = request.POST.getlist("toppings")
        
        p_extra = request.POST.get("extras")
        if p_extra is None:
            p_extra = 0
            #FiltroTopping = Topping.objects.filter(id__in=lista)
            precio = remplazo.replace(",",".")
            print(lista)
            print("No recogio p_extra")
            ordenes_instance = CartItems(
                username = user,
                nombre = nombre,
                precio = precio,
                t_lista = lista
            )
            ordenes_instance.save()
        else:
            L_extra = request.POST.get("n_extra")
            precio = remplazo.replace(",",".")
            precio_extra = p_extra.replace(",",".")
            print(L_extra)
            print("Recogio Precio de extra sub", precio_extra)
            total = float(precio) + float(precio_extra)
            ordenes_instance = CartItems(
                username = user,
                nombre = nombre,
                precio = total,
                t_lista = lista,
                l_extra = L_extra
            )
            ordenes_instance.save()

    return redirect('index')

def ordenes(request):
    user=request.user
    ordenes = CartItems.objects.all().filter(username=user)
    return render(request, 'cart/cart_detail.html',{"ordenes":ordenes})

def historial(request):

    user=request.user
    ordenes = CartItems.objects.all().filter(username=user, estado="True")
    return render(request, "Historial_compra.html",{"ordenes":ordenes})

@staff_member_required
def Admin(request):
    compras = CartItems.objects.all()
    return render(request, 'Admin.html', {"ordenes":compras})

@staff_member_required
def conf_envi(request, confirmar_id):

    ordenes = CartItems.objects.get(pk=confirmar_id)
    ordenes.Envio = "True"
    ordenes.save()
    return redirect('Admin')

def borrar_pedido(request, confirmar_id):
    ordenes = CartItems.objects.get(pk=confirmar_id)
    ordenes.delete()
    return redirect('Admin')
