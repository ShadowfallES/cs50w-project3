from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Topping)
admin.site.register(Categoria)
admin.site.register(TipoPizza)
admin.site.register(Product)
admin.site.register(CartItems)
admin.site.register(Extra)