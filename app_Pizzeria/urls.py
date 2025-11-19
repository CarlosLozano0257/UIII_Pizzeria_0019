from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # URL: Inicio
    # ==========================================
    # http://127.0.0.1:8019/
    path('', views.inicio_pizzeria, name='inicio_pizzeria'),

    # ==========================================
    # URLs: Proveedores
    # ==========================================
    # http://127.0.0.1:8019/proveedores/
    path('proveedores/', views.ver_proveedores, name='ver_proveedores'),
    # http://127.0.0.1:8019/proveedores/agregar/
    path('proveedores/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    # http://127.0.0.1:8019/proveedores/actualizar/ID/
    path('proveedores/actualizar/<int:id>/', views.actualizar_proveedor, name='actualizar_proveedor'),
    # (Esta URL no se ve, la usa el formulario de actualizar)
    path('proveedores/actualizar/realizar/', views.realizar_actualizacion_proveedor, name='realizar_actualizacion_proveedor'),
    # http://127.0.0.1:8019/proveedores/borrar/ID/
    path('proveedores/borrar/<int:id>/', views.borrar_proveedor, name='borrar_proveedor'),

    # ==========================================
    # URLs: Inventario
    # ==========================================
    # http://127.0.0.1:8019/inventario/
    path('inventario/', views.ver_inventario, name='ver_inventario'),
    # http://127.0.0.1:8019/inventario/agregar/
    path('inventario/agregar/', views.agregar_inventario, name='agregar_inventario'),
    # http://127.0.0.1:8019/inventario/actualizar/ID/
    path('inventario/actualizar/<int:id>/', views.actualizar_inventario, name='actualizar_inventario'),
    # (Esta URL no se ve, la usa el formulario de actualizar)
    path('inventario/actualizar/realizar/', views.realizar_actualizacion_inventario, name='realizar_actualizacion_inventario'),
    # http://127.0.0.1:8019/inventario/borrar/ID/
    path('inventario/borrar/<int:id>/', views.borrar_inventario, name='borrar_inventario'),

    # ==========================================
    # URLs: Menu
    # ==========================================
    # http://127.0.0.1:8019/menu/
    path('menu/', views.ver_menu, name='ver_menu'),
    # http://127.0.0.1:8019/menu/agregar/
    path('menu/agregar/', views.agregar_menu, name='agregar_menu'),
    # http://127.0.0.1:8019/menu/actualizar/ID/
    path('menu/actualizar/<int:id>/', views.actualizar_menu, name='actualizar_menu'),
    # (Esta URL no se ve, la usa el formulario de actualizar)
    path('menu/actualizar/realizar/', views.realizar_actualizacion_menu, name='realizar_actualizacion_menu'),
    # http://127.0.0.1:8019/menu/borrar/ID/
    path('menu/borrar/<int:id>/', views.borrar_menu, name='borrar_menu'),

    # ==========================================
    # URLs: Empleados (NUEVO)
    # ==========================================
    # http://127.0.0.1:8019/empleados/
    path('empleados/', views.ver_empleados, name='ver_empleados'),
    # http://127.0.0.1:8019/empleados/agregar/
    path('empleados/agregar/', views.agregar_empleado, name='agregar_empleado'),
    # http://127.0.0.1:8019/empleados/actualizar/ID/
    path('empleados/actualizar/<int:id>/', views.actualizar_empleado, name='actualizar_empleado'),
    # (Esta URL no se ve)
    path('empleados/actualizar/realizar/', views.realizar_actualizacion_empleado, name='realizar_actualizacion_empleado'),
    # http://127.0.0.1:8019/empleados/borrar/ID/
    path('empleados/borrar/<int:id>/', views.borrar_empleado, name='borrar_empleado'),

    # ==========================================
    # URLs: Promociones (NUEVO)
    # ==========================================
    # http://127.0.0.1:8019/promociones/
    path('promociones/', views.ver_promociones, name='ver_promociones'),
    # http://127.0.0.1:8019/promociones/agregar/
    path('promociones/agregar/', views.agregar_promocion, name='agregar_promocion'),
    # http://127.0.0.1:8019/promociones/actualizar/ID/
    path('promociones/actualizar/<int:id>/', views.actualizar_promocion, name='actualizar_promocion'),
    # (Esta URL no se ve)
    path('promociones/actualizar/realizar/', views.realizar_actualizacion_promocion, name='realizar_actualizacion_promocion'),
    # http://127.0.0.1:8019/promociones/borrar/ID/
    path('promociones/borrar/<int:id>/', views.borrar_promocion, name='borrar_promocion'),

    # ==========================================
    # URLs: Ventas (NUEVO)
    # ==========================================
    # http://127.0.0.1:8019/ventas/
    path('ventas/', views.ver_ventas, name='ver_ventas'),
    # http://127.0.0.1:8019/ventas/agregar/
    path('ventas/agregar/', views.agregar_venta, name='agregar_venta'),
    # http://127.0.0.1:8019/ventas/actualizar/ID/
    path('ventas/actualizar/<int:id>/', views.actualizar_venta, name='actualizar_venta'),
    # (Esta URL no se ve)
    path('ventas/actualizar/realizar/', views.realizar_actualizacion_venta, name='realizar_actualizacion_venta'),
    # http://127.0.0.1:8019/ventas/borrar/ID/
    path('ventas/borrar/<int:id>/', views.borrar_venta, name='borrar_venta'),
]