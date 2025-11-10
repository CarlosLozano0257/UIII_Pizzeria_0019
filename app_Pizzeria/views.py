from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedores, Inventario, Menu # <-- IMPORTANTE: Añadir Menu
import datetime # Necesario para el footer

# ==========================================
# VISTA: INICIO
# ==========================================
def inicio_pizzeria(request):
    """
    Vista para la página de inicio.
    """
    contexto = {
        'fecha_actual': datetime.date.today(),
    }
    return render(request, 'inicio.html', contexto)

# ==========================================
# VISTAS: PROVEEDORES
# ==========================================
def ver_proveedores(request):
    """
    Vista para mostrar todos los proveedores.
    """
    lista_proveedores = Proveedores.objects.all()
    contexto = {
        'proveedores': lista_proveedores,
        'fecha_actual': datetime.date.today(),
    }
    return render(request, 'proveedores/ver_proveedores.html', contexto)

def agregar_proveedor(request):
    """
    Vista para procesar la adición de un nuevo proveedor.
    """
    if request.method == 'POST':
        # Capturamos los datos del formulario
        nombre = request.POST.get('nombre_proveedor')
        telefono = request.POST.get('telefono_contacto')
        email = request.POST.get('email_contacto')
        direccion = request.POST.get('direccion')
        tipo = request.POST.get('tipo_producto')
        rfc = request.POST.get('rfc')
        
        # Creamos el nuevo proveedor
        Proveedores.objects.create(
            nombre_proveedor=nombre,
            telefono_contacto=telefono,
            email_contacto=email,
            direccion=direccion,
            tipo_producto=tipo,
            rfc=rfc
        )
        # Redirigimos a la lista de proveedores
        return redirect('ver_proveedores')
    
    # Si no es POST, solo mostramos la página (aunque usualmente se usa una vista separada para GET)
    # Por simplicidad del CRUD, asumimos que el formulario está en una página
    # y esta vista solo maneja el POST.
    # Para mostrar el formulario:
    contexto = {
        'fecha_actual': datetime.date.today(),
    }
    return render(request, 'proveedores/agregar_proveedor.html', contexto)


def actualizar_proveedor(request, id):
    """
    Vista para mostrar el formulario con los datos de un proveedor específico
    que se desea actualizar.
    """
    # Obtenemos el proveedor específico o mostramos error 404
    proveedor = get_object_or_404(Proveedores, id=id)
    
    contexto = {
        'proveedor': proveedor,
        'fecha_actual': datetime.date.today(),
    }
    return render(request, 'proveedores/actualizar_proveedor.html', contexto)

def realizar_actualizacion_proveedor(request):
    """
    Vista para procesar la actualización de un proveedor.
    Se accede a esta vista mediante POST desde 'actualizar_proveedor.html'.
    """
    if request.method == 'POST':
        # Obtenemos el ID del proveedor a actualizar
        id_proveedor = request.POST.get('id_proveedor')
        
        try:
            # Buscamos el proveedor
            proveedor = Proveedores.objects.get(id=id_proveedor)
            
            # Actualizamos los datos
            proveedor.nombre_proveedor = request.POST.get('nombre_proveedor')
            proveedor.telefono_contacto = request.POST.get('telefono_contacto')
            proveedor.email_contacto = request.POST.get('email_contacto')
            proveedor.direccion = request.POST.get('direccion')
            proveedor.tipo_producto = request.POST.get('tipo_producto')
            proveedor.rfc = request.POST.get('rfc')
            
            # Guardamos los cambios
            proveedor.save()

        except Proveedores.DoesNotExist:
            # (Manejo de error simple, solo volvemos)
            pass 
        
        # Redirigimos a la lista de proveedores
        return redirect('ver_proveedores')
    
    # Si no es POST, redirigir a la lista
    return redirect('ver_proveedores')

def borrar_proveedor(request, id):
    """
    Vista para confirmar y procesar la eliminación de un proveedor.
    """
    # Obtenemos el proveedor
    proveedor = get_object_or_404(Proveedores, id=id)
    
    if request.method == 'POST':
        # Si el método es POST, significa que confirmaron la eliminación
        proveedor.delete()
        return redirect('ver_proveedores')
    
    # Si es GET, mostramos la página de confirmación
    contexto = {
        'proveedor': proveedor,
        'fecha_actual': datetime.date.today(),
    }
    return render(request, 'proveedores/borrar_proveedor.html', contexto)


# ==========================================
# VISTAS: INVENTARIO (¡NUEVO!)
# ==========================================

def ver_inventario(request):
    """
    Vista para mostrar todos los artículos del inventario.
    """
    # Obtenemos todos los artículos
    articulos = Inventario.objects.all()
    
    # Obtenemos todos los proveedores (para el formulario de filtro, aunque no se pidió,
    # es útil para el <select> al agregar/actualizar)
    proveedores = Proveedores.objects.filter(activo=True)
    
    contexto = {
        'articulos': articulos,
        'proveedores': proveedores,
        'fecha_actual': datetime.date.today(),
    }
    return render(request, 'inventario/ver_inventario.html', contexto)

def agregar_inventario(request):
    """
    Vista para mostrar el formulario de agregar artículo y
    para procesar la adición de un nuevo artículo de inventario.
    """
    # Obtenemos los proveedores activos para el <select>
    proveedores = Proveedores.objects.filter(activo=True)
    
    if request.method == 'POST':
        # Capturamos los datos del formulario
        nombre = request.POST.get('nombre_articulo')
        stock = request.POST.get('stock', 0.0)
        unidad = request.POST.get('unidad')
        stock_minimo = request.POST.get('stock_minimo', 0.0)
        costo_unitario = request.POST.get('costo_unitario', 0.0)
        id_proveedor = request.POST.get('proveedor')

        # Manejamos la fecha (puede venir vacía)
        fecha_compra = request.POST.get('fecha_ultima_compra')
        if not fecha_compra:
            fecha_compra = None
            
        # Manejamos el proveedor (puede venir vacío)
        proveedor_obj = None
        if id_proveedor:
            try:
                proveedor_obj = Proveedores.objects.get(id=id_proveedor)
            except Proveedores.DoesNotExist:
                proveedor_obj = None

        # Creamos el nuevo artículo
        Inventario.objects.create(
            nombre_articulo=nombre,
            stock=stock,
            unidad=unidad,
            fecha_ultima_compra=fecha_compra,
            stock_minimo=stock_minimo,
            costo_unitario=costo_unitario,
            proveedor=proveedor_obj
        )
        
        # Redirigimos a la lista de inventario
        return redirect('ver_inventario')

    # Si es GET, solo mostramos el formulario
    contexto = {
        'proveedores': proveedores,
        'fecha_actual': datetime.date.today(),
    }
    return render(request, 'inventario/agregar_inventario.html', contexto)

def actualizar_inventario(request, id):
    """
    Vista para mostrar el formulario con los datos de un artículo específico
    que se desea actualizar.
    """
    # Obtenemos el artículo específico o mostramos error 404
    articulo = get_object_or_404(Inventario, id=id)
    # Obtenemos todos los proveedores para el <select>
    proveedores = Proveedores.objects.filter(activo=True)
    
    contexto = {
        'articulo': articulo,
        'proveedores': proveedores,
        'fecha_actual': datetime.date.today(),
    }
    return render(request, 'inventario/actualizar_inventario.html', contexto)

def realizar_actualizacion_inventario(request):
    """
    Vista para procesar la actualización de un artículo de inventario.
    Se accede a esta vista mediante POST desde 'actualizar_inventario.html'.
    """
    if request.method == 'POST':
        # Obtenemos el ID del artículo a actualizar
        id_articulo = request.POST.get('id_articulo')
        
        try:
            # Buscamos el artículo
            articulo = Inventario.objects.get(id=id_articulo)
            
            # Actualizamos los datos
            articulo.nombre_articulo = request.POST.get('nombre_articulo')
            articulo.stock = request.POST.get('stock', 0.0)
            articulo.unidad = request.POST.get('unidad')
            articulo.stock_minimo = request.POST.get('stock_minimo', 0.0)
            articulo.costo_unitario = request.POST.get('costo_unitario', 0.0)
            
            # Manejamos la fecha
            fecha_compra = request.POST.get('fecha_ultima_compra')
            articulo.fecha_ultima_compra = fecha_compra if fecha_compra else None
            
            # Manejamos el proveedor
            id_proveedor = request.POST.get('proveedor')
            if id_proveedor:
                try:
                    articulo.proveedor = Proveedores.objects.get(id=id_proveedor)
                except Proveedores.DoesNotExist:
                    articulo.proveedor = None
            else:
                articulo.proveedor = None
            
            # Guardamos los cambios
            articulo.save()

        except Inventario.DoesNotExist:
            # (Manejo de error simple, solo volvemos)
            pass 
        
        # Redirigimos a la lista de inventario
        return redirect('ver_inventario')
    
    # Si no es POST, redirigir a la lista
    return redirect('ver_inventario')

def borrar_inventario(request, id):
    """
    Vista para confirmar y procesar la eliminación de un artículo.
    """
    # Obtenemos el artículo
    articulo = get_object_or_404(Inventario, id=id)
    
    if request.method == 'POST':
        # Si el método es POST, significa que confirmaron la eliminación
        articulo.delete()
        return redirect('ver_inventario')
    
    # Si es GET, mostramos la página de confirmación
    contexto = {
        'articulo': articulo,
        'fecha_actual': datetime.date.today(),
    }
    return render(request, 'inventario/borrar_inventario.html', contexto)

# ==========================================
# VISTAS: MENÚ (¡NUEVO!)
# ==========================================

def ver_menu(request):
    """
    Vista para mostrar todos los productos del menú.
    """
    # Obtenemos todos los productos del menú
    productos = Menu.objects.all()
    
    contexto = {
        'productos': productos,
        'fecha_actual': datetime.date.today(),
    }
    return render(request, 'menu/ver_menu.html', contexto)

def agregar_menu(request):
    """
    Vista para mostrar el formulario de agregar producto y
    para procesar la adición de un nuevo producto al menú.
    """
    # Obtenemos todos los artículos de inventario para el <select>
    articulos_inventario = Inventario.objects.all()
    
    if request.method == 'POST':
        # Capturamos los datos del formulario
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio', 0.0)
        categoria = request.POST.get('categoria')
        tamaño = request.POST.get('tamaño')
        disponible = 'disponible' in request.POST # Checkbox

        # 1. Creamos el objeto Menu con los datos simples
        nuevo_producto = Menu.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            categoria=categoria,
            tamaño=tamaño,
            disponible=disponible
        )

        # 2. Obtenemos la lista de IDs de los artículos seleccionados
        articulos_ids = request.POST.getlist('articulos')

        # 3. Asignamos esos artículos al producto recién creado
        if articulos_ids:
            nuevo_producto.articulos.set(articulos_ids)
        
        # Redirigimos a la lista de menú
        return redirect('ver_menu')

    # Si es GET, solo mostramos el formulario
    contexto = {
        'articulos_inventario': articulos_inventario,
        'fecha_actual': datetime.date.today(),
    }
    return render(request, 'menu/agregar_menu.html', contexto)

def actualizar_menu(request, id):
    """
    Vista para mostrar el formulario con los datos de un producto específico
    que se desea actualizar.
    """
    # Obtenemos el producto específico
    producto = get_object_or_404(Menu, id=id)
    # Obtenemos todos los artículos para el <select>
    articulos_inventario = Inventario.objects.all()
    
    contexto = {
        'producto': producto,
        'articulos_inventario': articulos_inventario,
        'fecha_actual': datetime.date.today(),
    }
    return render(request, 'menu/actualizar_menu.html', contexto)

def realizar_actualizacion_menu(request):
    """
    Vista para procesar la actualización de un producto del menú.
    """
    if request.method == 'POST':
        # Obtenemos el ID del producto a actualizar
        id_producto = request.POST.get('id_producto')
        
        try:
            # Buscamos el producto
            producto = Menu.objects.get(id=id_producto)
            
            # 1. Actualizamos los datos simples
            producto.nombre = request.POST.get('nombre')
            producto.descripcion = request.POST.get('descripcion')
            producto.precio = request.POST.get('precio', 0.0)
            producto.categoria = request.POST.get('categoria')
            producto.tamaño = request.POST.get('tamaño')
            producto.disponible = 'disponible' in request.POST # Checkbox
            
            producto.save() # Guardamos los campos simples

            # 2. Actualizamos la relación ManyToMany
            articulos_ids = request.POST.getlist('articulos')
            producto.articulos.set(articulos_ids)

        except Menu.DoesNotExist:
            pass 
        
        # Redirigimos a la lista de menú
        return redirect('ver_menu')
    
    # Si no es POST, redirigir a la lista
    return redirect('ver_menu')

def borrar_menu(request, id):
    """
    Vista para confirmar y procesar la eliminación de un producto.
    """
    # Obtenemos el producto
    producto = get_object_or_404(Menu, id=id)
    
    if request.method == 'POST':
        # Si el método es POST, eliminamos
        producto.delete()
        return redirect('ver_menu')
    
    # Si es GET, mostramos la página de confirmación
    contexto = {
        'producto': producto,
        'fecha_actual': datetime.date.today(),
    }
    return render(request, 'menu/borrar_menu.html', contexto)