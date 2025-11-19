from django.contrib import admin
# Importamos los 6 modelos
from .models import Proveedores, Inventario, Menu, Empleados, Promociones, Ventas

# Registramos los modelos para que aparezcan en el panel de admin

# (Opcional: Clases para personalizar el admin)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_articulo', 'stock', 'unidad', 'proveedor', 'costo_unitario')
    list_filter = ('proveedor',)
    search_fields = ('nombre_articulo',)

class MenuAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'disponible')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre',)
    filter_horizontal = ('articulos',) # Mejora la interfaz de ManyToMany

class EmpleadosAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'puesto', 'telefono', 'email')
    search_fields = ('nombre_completo', 'puesto')

class VentasAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_hora', 'producto', 'cantidad', 'monto_total', 'empleado')
    list_filter = ('fecha_hora', 'empleado', 'producto')
    search_fields = ('producto__nombre', 'empleado__nombre_completo')
    autocomplete_fields = ('producto', 'empleado', 'promocion') # Facilita la búsqueda

class PromocionesAdmin(admin.ModelAdmin):
    list_display = ('nombre_promo', 'codigo_promo', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre_promo', 'codigo_promo')

# Registro final
admin.site.register(Proveedores)
admin.site.register(Inventario, InventarioAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Empleados, EmpleadosAdmin)
admin.site.register(Promociones, PromocionesAdmin)
admin.site.register(Ventas, VentasAdmin)