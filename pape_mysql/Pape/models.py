from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.text import slugify

#las categorias nos ayudaran a saber a que departamento pertenecen.
CATEGORIAS_SELECCIONADAS = (
    ('escolar','Escolar'),
    ('papel','Papel'),
    ('regalos','Regalos y Fiestas'),
    ('monografias','Monografias'),
)

CATEGORIAS_ETIQUETAS = (
    ('P','primary'),
    ('S','secondary'),
    ('D','danger')
)

CATEGORIAS_ESTATUS = (
    ('activo','primary'),
    ('inactivo','secondary'),
    ('eliminado','danger')
)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)    
    precio = models.DecimalField(max_digits=10, decimal_places=2 )
    precio_descuento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    categoria = models.CharField(choices=CATEGORIAS_SELECCIONADAS, max_length=20, default="escolar", blank="")
    estatus = models.CharField(choices=CATEGORIAS_ESTATUS, max_length=10, default="activo")
    lugar = models.CharField(max_length=5, blank=True)
    etiqueta = models.CharField(choices=CATEGORIAS_ETIQUETAS, max_length=1, default="P")
    slug = models.SlugField(unique=True, null=False, blank=True, max_length=255)
    descripcion = models.TextField(default="Aquí sustituimos la descripción del producto")    
    imagen = models.ImageField(default='default.jpg', upload_to='img_productos')
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def url_absoluta(self):
        return reverse("producto", kwargs={"slug":self.slug})      
    
    def url_categoria(self):
        return reverse("categorias", kwargs={"categoria":self.categoria})      
    
    def url_agregar_carrito(self):
        return reverse("agregar_carrito", kwargs={"slug":self.slug})
    
    def url_remover_carrito(self):
        return reverse("remover_carrito", kwargs={"slug":self.slug})

    def __str__(self):
        return self.nombre


class Producto_Ordenado(models.Model):
    #Aqui asociamos el usuario logeado a la orden
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    #Aqui Se trae el nombre del producto de la tabla Prodcuto
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    ordenado = models.BooleanField(default=False)

    def total_precio_normal(self):
        return self.cantidad * self.producto.precio
    
    def total_precio_descuento(self):
        return self.cantidad * self.producto.precio_descuento
    
    def total_ahorrado(self):
        return self.total_precio_normal() -  self.total_precio_descuento()
    
    def precio_final(self):
        if self.producto.precio_descuento:
            return self.total_precio_descuento()
        return self.total_precio_normal()

    def __str__(self):
        return f"{self.cantidad} - {self.producto.nombre}"


class Orden(models.Model):
    #Aqui asociamos el usuario logeado a la orden
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    #Este campo deberia acpetar todos los productos ordenados en la orden.
    productos = models.ManyToManyField(Producto_Ordenado)
    fecha_actual = models.DateTimeField(auto_now_add=True)
    fecha_orden = models.DateTimeField()
    ordenado = models.BooleanField(default=False)

    def total(self):
        total = 0
        for articulo in self.productos.all():
            total += articulo.precio_final()
        return total 

    def __str__(self):
        return self.usuario.username


"""
class Producto(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    nombre = models.CharField(max_length=255)
    # otros campos aquí

    def save(self, *args, **kwargs):
        if not self.id:
            last_id = Producto.objects.order_by('-id').first()
            if last_id:
                self.id = last_id.id + 1
            else:
                self.id = 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detalle-producto', args=[str(self.id)]) 
"""