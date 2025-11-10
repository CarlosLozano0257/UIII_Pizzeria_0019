from django.contrib import admin
from .models import Proveedores, Inventario, Menu # Asegúrate de importar todos

# Registramos los modelos para que aparezcan en el panel de admin

# Configuración básica para Proveedores
@admin.register(Proveedores)
class ProveedoresAdmin(admin.ModelAdmin):
    list_display = ('nombre_proveedor', 'telefono_contacto', 'email_contacto', 'activo')
    list_filter = ('activo', 'tipo_producto')
    search_fields = ('nombre_proveedor', 'rfc')

# Configuración básica para Inventario (¡NUEVO!)
@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_articulo', 'stock', 'unidad', 'costo_unitario', 'proveedor', 'fecha_ultima_compra')
    list_filter = ('unidad', 'proveedor')
    search_fields = ('nombre_articulo',)

# Configuración básica para Menu (¡NUEVO!)
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'tamaño', 'disponible')
    list_filter = ('categoria', 'disponible', 'tamaño')
    search_fields = ('nombre',)
    # Para campos ManyToMany, se recomienda filter_horizontal
    filter_horizontal = ('articulos',)