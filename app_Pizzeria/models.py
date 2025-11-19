from django.db import models

# ==========================================
# MODELO: Proveedores
# ==========================================
class Proveedores(models.Model):
    # id_proveedor es automático (AutoField)
    nombre_proveedor = models.CharField(max_length=100, unique=True)
    telefono_contacto = models.CharField(max_length=15, blank=True, null=True)
    email_contacto = models.EmailField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    tipo_producto = models.CharField(max_length=100, blank=True, null=True)
    rfc = models.CharField(max_length=20, blank=True, null=True, unique=True, help_text="RFC del proveedor (único)")
    fecha_registro = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_proveedor

# ==========================================
# MODELO: Inventario
# ==========================================
class Inventario(models.Model):
    # id_articulo es automático (AutoField)
    nombre_articulo = models.CharField(max_length=100)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    unidad = models.CharField(max_length=20) # Ej: 'kg', 'litro', 'pieza'
    fecha_ultima_compra = models.DateField(null=True, blank=True)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    # Relación: Un artículo de inventario pertenece a UN proveedor
    proveedor = models.ForeignKey(
        Proveedores, 
        on_delete=models.SET_NULL, # Si se borra el proveedor, el artículo no se borra
        null=True, 
        blank=True, 
        related_name="articulos_inventario",
        db_column="fk_id_proveedor" # Coincide con tu diagrama
    )

    def __str__(self):
        return f"{self.nombre_articulo} ({self.stock} {self.unidad})"

# ==========================================
# MODELO: Menu
# ==========================================
class Menu(models.Model):
    # id_producto es automático (AutoField)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50) # Ej: 'Bebida', 'Postre', 'Pizza'
    tamaño = models.CharField(max_length=50, blank=True, null=True) # Ej: 'Chico', 'Grande'
    disponible = models.BooleanField(default=True)

    # Relación: Un producto del menú (ej: Pizza) usa VARIOS artículos del inventario (ej: Harina, Queso)
    articulos = models.ManyToManyField(
        Inventario,
        related_name="productos_menu",
        blank=True # Un producto puede existir sin artículos
    )

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

# ==========================================
# MODELO: Promociones (NUEVO)
# ==========================================
class Promociones(models.Model):
    # id_promo es automático (AutoField)
    nombre_promo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    codigo_promo = models.CharField(max_length=20, blank=True, null=True, unique=True)
    precio_especial = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Ej: 'Activa', 'Inactiva', 'Vencida'
    estado = models.CharField(max_length=20, default='Activa')

    def __str__(self):
        return self.nombre_promo

# ==========================================
# MODELO: Empleados (NUEVO)
# ==========================================
class Empleados(models.Model):
    # id_empleado es automático (AutoField)
    nombre_completo = models.CharField(max_length=150)
    puesto = models.CharField(max_length=50) # Ej: 'Cajero', 'Cocinero', 'Repartidor'
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    fecha_contratacion = models.DateField()
    direccion = models.CharField(max_length=255, blank=True, null=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nombre_completo} ({self.puesto})"

# ==========================================
# MODELO: Ventas (NUEVO)
# ==========================================
class Ventas(models.Model):
    # id_venta es automático (AutoField)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    cantidad = models.IntegerField(default=1)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50, default='Efectivo') # Ej: 'Efectivo', 'Tarjeta'

    # Relación: La venta fue registrada por UN Empleado
    empleado = models.ForeignKey(
        Empleados,
        on_delete=models.SET_NULL, # Si se borra el empleado, la venta no se borra
        null=True,
        blank=True,
        db_column="fk_id_empleado"
    )
    
    # Relación: La venta fue de UN Producto del Menú
    producto = models.ForeignKey(
        Menu,
        on_delete=models.SET_NULL, # Si se borra el producto, la venta no se borra
        null=True,
        blank=True,
        db_column="fk_id_producto"
    )

    # Relación: La venta (opcionalmente) usó UNA Promoción
    promocion = models.ForeignKey(
        Promociones,
        on_delete=models.SET_NULL, # Si se borra la promo, la venta no se borra
        null=True,
        blank=True,
        db_column="fk_id_promo"
    )

    def __str__(self):
        return f"Venta #{self.id} - {self.producto.nombre if self.producto else 'N/A'} - ${self.monto_total}"