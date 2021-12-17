import re
import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.base import Model
import datetime

from django.db.models.fields import DecimalField


# Create your models here.
# Modelo de la Categoria
class Categoria(models.Model):

    Categoria=models.CharField(max_length=200)
    
    def __str__(self):
        return self.Categoria

# Modelo de topping
class Topping(models.Model):

    Topping=models.CharField(max_length=100)

    def __str__(self):
        return self.Topping

# Modelo de tabla sobre la tipo de pizza
class TipoPizza(models.Model):
    TipoPizza=models.CharField(max_length=20)

    def __str__(self):
        return self.TipoPizza

class Extra(models.Model):
    Extra = models.CharField(max_length=30, blank=False, null=False)
    Precio = models.DecimalField(max_digits=5, decimal_places=2, null=False,blank=False)

    def __str__(self):
        return self.Extra

# Funcion para subir imagenes de los platillos  
def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%I:%M')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('static/uploads/', filename)

class Product(models.Model):
    name=models.CharField(max_length=100)
    Categoria = models.ForeignKey(Categoria, null=True, on_delete=models.CASCADE)
    TipoPizza = models.ForeignKey(TipoPizza, null=True , blank=True,on_delete=models.CASCADE)
    Precio = models.DecimalField(max_digits=5, decimal_places=2, null=True,blank=True)
    P_Small = models.DecimalField(max_digits=5, decimal_places=2, null=True,blank=True)
    P_Large = models.DecimalField(max_digits=5, decimal_places=2, null=True,blank=True)
    Extra = models.ForeignKey(Extra, null=True, blank=True, on_delete=models.CASCADE)
    img_producto = models.ImageField(upload_to=filepath, null=True, blank=True) 
    Topping_Estado = models.BooleanField(default=False)
    total_toppings = models.IntegerField(null=False,blank=False,default="0")
    Extra_Estado = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class CartItems(models.Model):
    username = models.CharField("Cliente", max_length=50,null=False,blank=False)
    nombre = models.CharField("Producto", max_length=30, null=False, blank=False)
    cantidad = models.IntegerField("Cantidad del producto:", default=1)
    precio = DecimalField(max_digits=5, decimal_places=2, null=True,blank=True)
    t_lista = models.CharField("Toppings", max_length=100,null=True,blank=True, default=' ')
    l_extra = models.CharField("Extras", max_length=100,null=True,blank=True, default=' ')
    estado = models.BooleanField("Confirmacion de compra",default=False)
    Envio = models.BooleanField("Confirmacion de Envio",default=False)
    def __str__(self):
        return str(self.username)

