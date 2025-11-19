from django.shortcuts import render, redirect, get_object_or_404
# IMPORTAMOS LOS 6 MODELOS
from .models import Proveedores, Inventario, Menu, Promociones, Empleados, Ventas

# ==========================================
# VISTA: Inicio
# ==========================================
def inicio_pizzeria(request):
    # Contar el total de registros de cada modelo
    total_proveedores = Proveedores.objects.count()
    total_inventario = Inventario.objects.count()
    total_menu = Menu.objects.count()
    total_empleados = Empleados.objects.count()
    total_promociones = Promociones.objects.count()
    total_ventas = Ventas.objects.count()

    contexto = {
        'total_proveedores': total_proveedores,
        'total_inventario': total_inventario,
        'total_menu': total_menu,
        'total_empleados': total_empleados,
        'total_promociones': total_promociones,
        'total_ventas': total_ventas,
    }
    return render(request, 'inicio.html', contexto)

# ==========================================
# CRUD: Proveedores
# ==========================================

# 1. Ver (Read)
def ver_proveedores(request):
    proveedores = Proveedores.objects.all()
    return render(request, 'proveedores/ver_proveedores.html', {'proveedores': proveedores})

# 2. Agregar (Create)
def agregar_proveedor(request):
    if request.method == "POST":
        nombre = request.POST['nombre_proveedor']
        telefono = request.POST['telefono_contacto']
        email = request.POST['email_contacto']
        direccion = request.POST['direccion']
        tipo_producto = request.POST['tipo_producto']
        rfc = request.POST['rfc']
        
        # Guardar en la BD
        proveedor = Proveedores(
            nombre_proveedor=nombre,
            telefono_contacto=telefono,
            email_contacto=email,
            direccion=direccion,
            tipo_producto=tipo_producto,
            rfc=rfc
        )
        proveedor.save()
        return redirect('ver_proveedores')
        
    return render(request, 'proveedores/agregar_proveedor.html')

# 3. Actualizar (Update) - Paso 1: Mostrar formulario con datos
def actualizar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedores, id=id)
    return render(request, 'proveedores/actualizar_proveedor.html', {'proveedor': proveedor})

# 3. Actualizar (Update) - Paso 2: Recibir y guardar datos
def realizar_actualizacion_proveedor(request):
    if request.method == "POST":
        id_proveedor = request.POST['id_proveedor']
        proveedor = get_object_or_404(Proveedores, id=id_proveedor)
        
        # Actualizar campos
        proveedor.nombre_proveedor = request.POST['nombre_proveedor']
        proveedor.telefono_contacto = request.POST['telefono_contacto']
        proveedor.email_contacto = request.POST['email_contacto']
        proveedor.direccion = request.POST['direccion']
        proveedor.tipo_producto = request.POST['tipo_producto']
        proveedor.rfc = request.POST['rfc']
        
        proveedor.save()
        return redirect('ver_proveedores')
    
    return redirect('ver_proveedores') # Redirigir si no es POST

# 4. Borrar (Delete)
def borrar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedores, id=id)
    
    if request.method == "POST":
        proveedor.delete()
        return redirect('ver_proveedores')
        
    return render(request, 'proveedores/borrar_proveedor.html', {'proveedor': proveedor})

# ==========================================
# CRUD: Inventario
# ==========================================

# 1. Ver (Read)
def ver_inventario(request):
    articulos = Inventario.objects.all()
    return render(request, 'inventario/ver_inventario.html', {'articulos': articulos})

# 2. Agregar (Create)
def agregar_inventario(request):
    if request.method == "POST":
        nombre = request.POST['nombre_articulo']
        unidad = request.POST['unidad']
        stock = request.POST['stock']
        stock_minimo = request.POST['stock_minimo']
        costo = request.POST['costo_unitario']
        fecha = request.POST['fecha_ultima_compra']
        id_proveedor = request.POST['proveedor']
        
        proveedor = None
        if id_proveedor:
            proveedor = get_object_or_404(Proveedores, id=id_proveedor)
            
        if not fecha:
            fecha = None

        articulo = Inventario(
            nombre_articulo=nombre,
            unidad=unidad,
            stock=stock,
            stock_minimo=stock_minimo,
            costo_unitario=costo,
            fecha_ultima_compra=fecha,
            proveedor=proveedor
        )
        articulo.save()
        return redirect('ver_inventario')
    
    proveedores = Proveedores.objects.all()
    return render(request, 'inventario/agregar_inventario.html', {'proveedores': proveedores})

# 3. Actualizar (Update) - Paso 1: Mostrar formulario
def actualizar_inventario(request, id):
    articulo = get_object_or_404(Inventario, id=id)
    proveedores = Proveedores.objects.all()
    contexto = {
        'articulo': articulo,
        'proveedores': proveedores
    }
    return render(request, 'inventario/actualizar_inventario.html', contexto)

# 3. Actualizar (Update) - Paso 2: Guardar
def realizar_actualizacion_inventario(request):
    if request.method == "POST":
        id_articulo = request.POST['id_articulo']
        articulo = get_object_or_404(Inventario, id=id_articulo)
        
        articulo.nombre_articulo = request.POST['nombre_articulo']
        articulo.unidad = request.POST['unidad']
        articulo.stock = request.POST['stock']
        articulo.stock_minimo = request.POST['stock_minimo']
        articulo.costo_unitario = request.POST['costo_unitario']
        fecha = request.POST['fecha_ultima_compra']
        id_proveedor = request.POST['proveedor']
        
        proveedor = None
        if id_proveedor:
            proveedor = get_object_or_404(Proveedores, id=id_proveedor)
            
        if not fecha:
            articulo.fecha_ultima_compra = None
        else:
            articulo.fecha_ultima_compra = fecha
            
        articulo.proveedor = proveedor
        articulo.save()
        return redirect('ver_inventario')
        
    return redirect('ver_inventario')

# 4. Borrar (Delete)
def borrar_inventario(request, id):
    articulo = get_object_or_404(Inventario, id=id)
    if request.method == "POST":
        articulo.delete()
        return redirect('ver_inventario')
        
    return render(request, 'inventario/borrar_inventario.html', {'articulo': articulo})

# ==========================================
# CRUD: Menu
# ==========================================

# 1. Ver (Read)
def ver_menu(request):
    productos = Menu.objects.all()
    return render(request, 'menu/ver_menu.html', {'productos': productos})

# 2. Agregar (Create)
def agregar_menu(request):
    if request.method == "POST":
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        categoria = request.POST['categoria']
        tamaño = request.POST['tamaño']
        disponible = 'disponible' in request.POST
        
        # IDs de los artículos seleccionados
        ids_articulos = request.POST.getlist('articulos')
        
        nuevo_producto = Menu.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            categoria=categoria,
            tamaño=tamaño,
            disponible=disponible
        )
        
        # Asignar los artículos de inventario
        if ids_articulos:
            articulos_inventario = Inventario.objects.filter(id__in=ids_articulos)
            nuevo_producto.articulos.set(articulos_inventario)
            
        return redirect('ver_menu')
        
    articulos_inventario = Inventario.objects.all()
    return render(request, 'menu/agregar_menu.html', {'articulos_inventario': articulos_inventario})

# 3. Actualizar (Update) - Paso 1: Mostrar formulario
def actualizar_menu(request, id):
    producto = get_object_or_404(Menu, id=id)
    articulos_inventario = Inventario.objects.all()
    
    # IDs de los artículos que este producto YA tiene
    ids_articulos_actuales = producto.articulos.all().values_list('id', flat=True)
    
    contexto = {
        'producto': producto,
        'articulos_inventario': articulos_inventario,
        'ids_articulos_actuales': ids_articulos_actuales
    }
    return render(request, 'menu/actualizar_menu.html', contexto)

# 3. Actualizar (Update) - Paso 2: Guardar
def realizar_actualizacion_menu(request):
    if request.method == "POST":
        id_producto = request.POST['id_producto']
        producto = get_object_or_404(Menu, id=id_producto)
        
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST['descripcion']
        producto.precio = request.POST['precio']
        producto.categoria = request.POST['categoria']
        producto.tamaño = request.POST['tamaño']
        producto.disponible = 'disponible' in request.POST
        
        # IDs de los artículos seleccionados en el formulario
        ids_articulos = request.POST.getlist('articulos')
        
        # Actualizar los artículos de inventario
        if ids_articulos:
            articulos_inventario = Inventario.objects.filter(id__in=ids_articulos)
            producto.articulos.set(articulos_inventario)
        else:
            # Si no se seleccionó ninguno, se quitan todas las relaciones
            producto.articulos.clear()
            
        producto.save()
        return redirect('ver_menu')
        
    return redirect('ver_menu')

# 4. Borrar (Delete)
def borrar_menu(request, id):
    producto = get_object_or_404(Menu, id=id)
    if request.method == "POST":
        producto.delete()
        return redirect('ver_menu')
        
    return render(request, 'menu/borrar_menu.html', {'producto': producto})

# ==========================================
# CRUD: Empleados (NUEVO)
# ==========================================

# 1. Ver (Read)
def ver_empleados(request):
    empleados = Empleados.objects.all()
    return render(request, 'empleados/ver_empleados.html', {'empleados': empleados})

# 2. Agregar (Create)
def agregar_empleado(request):
    if request.method == "POST":
        Empleados.objects.create(
            nombre_completo=request.POST['nombre_completo'],
            puesto=request.POST['puesto'],
            telefono=request.POST['telefono'],
            email=request.POST['email'],
            fecha_contratacion=request.POST['fecha_contratacion'],
            direccion=request.POST['direccion'],
            salario=request.POST['salario']
        )
        return redirect('ver_empleados')
    return render(request, 'empleados/agregar_empleado.html')

# 3. Actualizar (Update) - Paso 1: Mostrar formulario
def actualizar_empleado(request, id):
    empleado = get_object_or_404(Empleados, id=id)
    return render(request, 'empleados/actualizar_empleado.html', {'empleado': empleado})

# 3. Actualizar (Update) - Paso 2: Guardar
def realizar_actualizacion_empleado(request):
    if request.method == "POST":
        id_empleado = request.POST['id_empleado']
        empleado = get_object_or_404(Empleados, id=id_empleado)
        
        empleado.nombre_completo = request.POST['nombre_completo']
        empleado.puesto = request.POST['puesto']
        empleado.telefono = request.POST['telefono']
        empleado.email = request.POST['email']
        empleado.fecha_contratacion = request.POST['fecha_contratacion']
        empleado.direccion = request.POST['direccion']
        empleado.salario = request.POST['salario']
        
        empleado.save()
        return redirect('ver_empleados')
    return redirect('ver_empleados')

# 4. Borrar (Delete)
def borrar_empleado(request, id):
    empleado = get_object_or_404(Empleados, id=id)
    if request.method == "POST":
        empleado.delete()
        return redirect('ver_empleados')
    return render(request, 'empleados/borrar_empleado.html', {'empleado': empleado})

# ==========================================
# CRUD: Promociones (NUEVO)
# ==========================================

# 1. Ver (Read)
def ver_promociones(request):
    promociones = Promociones.objects.all()
    return render(request, 'promociones/ver_promociones.html', {'promociones': promociones})

# 2. Agregar (Create)
def agregar_promocion(request):
    if request.method == "POST":
        Promociones.objects.create(
            nombre_promo=request.POST['nombre_promo'],
            descripcion=request.POST['descripcion'],
            fecha_inicio=request.POST['fecha_inicio'],
            fecha_fin=request.POST['fecha_fin'],
            codigo_promo=request.POST['codigo_promo'],
            precio_especial=request.POST['precio_especial'] or None, # Si está vacío, guarda Null
            estado=request.POST['estado']
        )
        return redirect('ver_promociones')
    return render(request, 'promociones/agregar_promocion.html')

# 3. Actualizar (Update) - Paso 1: Mostrar formulario
def actualizar_promocion(request, id):
    promocion = get_object_or_404(Promociones, id=id)
    return render(request, 'promociones/actualizar_promocion.html', {'promocion': promocion})

# 3. Actualizar (Update) - Paso 2: Guardar
def realizar_actualizacion_promocion(request):
    if request.method == "POST":
        id_promo = request.POST['id_promo']
        promocion = get_object_or_404(Promociones, id=id_promo)
        
        promocion.nombre_promo = request.POST['nombre_promo']
        promocion.descripcion = request.POST['descripcion']
        promocion.fecha_inicio = request.POST['fecha_inicio']
        promocion.fecha_fin = request.POST['fecha_fin']
        promocion.codigo_promo = request.POST['codigo_promo']
        promocion.precio_especial = request.POST['precio_especial'] or None
        promocion.estado = request.POST['estado']
        
        promocion.save()
        return redirect('ver_promociones')
    return redirect('ver_promociones')

# 4. Borrar (Delete)
def borrar_promocion(request, id):
    promocion = get_object_or_404(Promociones, id=id)
    if request.method == "POST":
        promocion.delete()
        return redirect('ver_promociones')
    return render(request, 'promociones/borrar_promocion.html', {'promocion': promocion})

# ==========================================
# CRUD: Ventas (NUEVO)
# ==========================================

# 1. Ver (Read)
def ver_ventas(request):
    ventas = Ventas.objects.all().order_by('-fecha_hora') # Más recientes primero
    return render(request, 'ventas/ver_ventas.html', {'ventas': ventas})

# 2. Agregar (Create)
def agregar_venta(request):
    if request.method == "POST":
        id_empleado = request.POST['empleado']
        id_producto = request.POST['producto']
        id_promo = request.POST['promocion']
        
        empleado = get_object_or_404(Empleados, id=id_empleado)
        producto = get_object_or_404(Menu, id=id_producto)
        
        promocion = None
        if id_promo:
            promocion = get_object_or_404(Promociones, id=id_promo)

        Ventas.objects.create(
            empleado=empleado,
            producto=producto,
            promocion=promocion,
            cantidad=request.POST['cantidad'],
            monto_total=request.POST['monto_total'],
            metodo_pago=request.POST['metodo_pago']
        )
        return redirect('ver_ventas')
        
    # Enviar datos para los <select> del formulario
    contexto = {
        'empleados': Empleados.objects.all(),
        'productos': Menu.objects.filter(disponible=True),
        'promociones': Promociones.objects.filter(estado='Activa')
    }
    return render(request, 'ventas/agregar_venta.html', contexto)

# 3. Actualizar (Update) - Paso 1: Mostrar formulario
def actualizar_venta(request, id):
    venta = get_object_or_404(Ventas, id=id)
    contexto = {
        'venta': venta,
        'empleados': Empleados.objects.all(),
        'productos': Menu.objects.all(), # Mostrar todos por si el producto ya no está disponible
        'promociones': Promociones.objects.all() # Mostrar todas
    }
    return render(request, 'ventas/actualizar_venta.html', contexto)

# 3. Actualizar (Update) - Paso 2: Guardar
def realizar_actualizacion_venta(request):
    if request.method == "POST":
        id_venta = request.POST['id_venta']
        venta = get_object_or_404(Ventas, id=id_venta)
        
        id_empleado = request.POST['empleado']
        id_producto = request.POST['producto']
        id_promo = request.POST['promocion']
        
        venta.empleado = get_object_or_404(Empleados, id=id_empleado)
        venta.producto = get_object_or_404(Menu, id=id_producto)
        
        venta.promocion = None
        if id_promo:
            venta.promocion = get_object_or_404(Promociones, id=id_promo)
            
        venta.cantidad = request.POST['cantidad']
        venta.monto_total = request.POST['monto_total']
        venta.metodo_pago = request.POST['metodo_pago']
        
        venta.save()
        return redirect('ver_ventas')
    return redirect('ver_ventas')

# 4. Borrar (Delete)
def borrar_venta(request, id):
    venta = get_object_or_404(Ventas, id=id)
    if request.method == "POST":
        venta.delete()
        return redirect('ver_ventas')
    return render(request, 'ventas/borrar_venta.html', {'venta': venta})