from django import forms
from django import contrib
from django.http import HttpResponseRedirect, HttpResponse, request
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.urls import reverse
from django.contrib.auth import authenticate, logout as core_logout, login as auth_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .form import RegistroForm
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
    if response.method == 'POST':
        form = RegistroForm(response.POST)
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            messages.success(response, ("Registro completado"))
            return redirect('index')
    else:
        form = RegistroForm()
    return  render(response, 'register.html', {'form':form})

# Login de usuario
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        print(form)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            name = request.user
            messages.success(request, ("Bienvenido " + str(name)))
            return redirect('index')

    else:
        
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})

# Logout para el usuario
def logout(request):

    if request.method == 'POST':
        core_logout(request)
        messages.success(request, ("Adios, Vuelva pronto"))
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
    messages.success(request, ("Hemos agregado al carrito el plato " + str(nombre_producto)))
    return redirect("index")

@login_required(login_url="/login")
def confirmar(request, id_cart):
    ordenes = CartItems.objects.get(pk=id_cart)
    ordenes.estado = "True"
    ordenes.save()
    return redirect('ordenes')

@login_required(login_url="/login")
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
        if remplazo is None:
            messages.success(request, ("Por favor escoger el precio del plato!"))
            return redirect('index')
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
    messages.success(request, ("Hemos agregado al carrito el plato " + str(nombre)))
    return redirect('index')

@login_required(login_url="/login")
def ordenes(request):
    user=request.user
    ordenes = CartItems.objects.all().filter(username=user)
    return render(request, 'cart/cart_detail.html',{"ordenes":ordenes})

@login_required(login_url="/login")
def historial(request):

    user=request.user
    ordenes = CartItems.objects.all().filter(username=user, estado="True")
    return render(request, "Historial_compra.html",{"ordenes":ordenes})

@staff_member_required
def Admin(request):
    compras = CartItems.objects.all()
    return render(request, 'admin_pedido.html', {"ordenes":compras})

@staff_member_required
def conf_envi(request, confirmar_id):

    ordenes = CartItems.objects.get(pk=confirmar_id)
    ordenes.Envio = True
    ordenes.save()
    return redirect('Admin')

@login_required(login_url="/login")
def borrar_pedido(request, confirmar_id):
    ordenes = CartItems.objects.get(pk=confirmar_id)
    ordenes.delete()
    return redirect('Admin')

@staff_member_required
def Administracion(request):
    menu = Product.objects.all()
    topping = Topping.objects.all()
    extra = Extra.objects.all()
    return render(request, "Administracion.html", {"menu":menu, "topping":topping, "extra":extra})

# Borrar
@login_required(login_url="/login")
def borrar_menu(request, confirmar_id):
    producto = Product.objects.get(pk=confirmar_id)
    producto.delete()
    return redirect('Administracion')

@login_required(login_url="/login")
def borrar_Topping(request, confirmar_id):
    Toppings = Topping.objects.get(pk=confirmar_id)
    Toppings.delete()
    return redirect('Administracion')

@login_required(login_url="/login")
def borrar_extra(request, confirmar_id):
    extra = Extra.objects.get(pk=confirmar_id)
    extra.delete()
    return redirect('Administracion')