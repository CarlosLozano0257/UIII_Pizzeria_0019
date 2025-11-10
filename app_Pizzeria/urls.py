from django.urls import path
from . import views

urlpatterns = [
    # URLs de la App (Inicio)
    path('', views.inicio_pizzeria, name='inicio_pizzeria'),

    # URLs de Proveedores (CRUD)
    path('proveedores/', views.ver_proveedores, name='ver_proveedores'),
    path('proveedores/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/actualizar/<int:id>/', views.actualizar_proveedor, name='actualizar_proveedor'),
    path('proveedores/actualizar/realizar/', views.realizar_actualizacion_proveedor, name='realizar_actualizacion_proveedor'),
    path('proveedores/borrar/<int:id>/', views.borrar_proveedor, name='borrar_proveedor'),

    # URLs de Inventario (CRUD) (¡NUEVO!)
    path('inventario/', views.ver_inventario, name='ver_inventario'),
    path('inventario/agregar/', views.agregar_inventario, name='agregar_inventario'),
    path('inventario/actualizar/<int:id>/', views.actualizar_inventario, name='actualizar_inventario'),
    path('inventario/actualizar/realizar/', views.realizar_actualizacion_inventario, name='realizar_actualizacion_inventario'),
    path('inventario/borrar/<int:id>/', views.borrar_inventario, name='borrar_inventario'),
    
    # URLs de Menú (CRUD) (¡NUEVO!)
    path('menu/', views.ver_menu, name='ver_menu'),
    path('menu/agregar/', views.agregar_menu, name='agregar_menu'),
    path('menu/actualizar/<int:id>/', views.actualizar_menu, name='actualizar_menu'),
    path('menu/actualizar/realizar/', views.realizar_actualizacion_menu, name='realizar_actualizacion_menu'),
    path('menu/borrar/<int:id>/', views.borrar_menu, name='borrar_menu'),
]