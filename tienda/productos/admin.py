from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('fecha_creacion',)
