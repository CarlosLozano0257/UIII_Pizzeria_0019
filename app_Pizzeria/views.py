from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedores, Inventario # <-- IMPORTANTE: Añadir Inventario
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