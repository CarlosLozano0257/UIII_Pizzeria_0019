from django.db import models

# ==========================================
# MODELO: Proveedores (Actualizado)
# ==========================================
class Proveedores(models.Model):
    # id_proveedor es automático (AutoField)
    nombre_proveedor = models.CharField(max_length=100, unique=True)
    telefono_contacto = models.CharField(max_length=15, blank=True, null=True)
    email_contacto = models.EmailField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    tipo_producto = models.CharField(max_length=100, blank=True, null=True)
    rfc = models.CharField(max_length=20, blank=True, null=True, unique=True) # RFC debería ser único si existe
    fecha_registro = models.DateField(auto_now_add=True) # auto_now_add es útil para la fecha de registro
    activo = models.BooleanField(default=True) # Conservado del modelo original

    def __str__(self):
        return self.nombre_proveedor # Actualizado para que coincida con el nuevo nombre de campo

# ==========================================
# MODELO: Inventario (Nuevo)
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
        on_delete=models.SET_NULL, # Si se borra el proveedor, el artículo no se borra, solo se quita la relación
        null=True, 
        blank=True, 
        related_name="articulos_inventario",
        db_column="fk_id_proveedor" # Coincide con tu diagrama
    )

    def __str__(self):
        return f"{self.nombre_articulo} ({self.stock} {self.unidad})"

# ==========================================
# MODELO: Menu (Nuevo)
# ==========================================
class Menu(models.Model):
    # id_producto es automático (AutoField)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50) # Ej: 'Bebida', 'Postre', 'Plato Fuerte'
    tamaño = models.CharField(max_length=50, blank=True, null=True) # Ej: 'Chico', 'Grande'
    disponible = models.BooleanField(default=True)

    # Relación (Como solicitaste):
    # Un producto del menú (ej: Hamburguesa) usa VARIOS artículos del inventario (ej: Pan, Carne, Queso)
    # Y un artículo del inventario (ej: Queso) puede ser usado en VARIOS productos del menú (ej: Hamburguesa, Nachos)
    articulos = models.ManyToManyField(
        Inventario,
        related_name="productos_menu",
        blank=True # Un producto puede existir sin artículos de inventario definidos
    )

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"