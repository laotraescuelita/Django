from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from .models import Producto, Orden, Producto_Ordenado

import json
from django.http import HttpResponse
def cargar_productos(request):
    with open('C:\\Users\\erick\\OneDrive\\Escritorio\\Cpanel_Pape\\Pape_Diana\\Tienda\\Pape\\productos.json', 'r') as archivo:
        datos = json.load(archivo)

    for dato in datos:
        producto = Producto(
        
        nombre=dato['nombre'],
        precio=dato['precio'],
        precio_descuento=dato['precio_descuento'],
        categoria=dato['categoria'],
        estatus=dato['estatus'],
        lugar=dato['lugar'],
        etiqueta=dato['etiqueta'],
        slug=dato['slug'],
        descripcion=dato['descripcion']
        
         )
        producto.save()

    return HttpResponse('Los productos se han cargado exitosamente en la base de datos.')


class InicioView(ListView):
    model = Producto
    template_name = "Pape/inicio.html"
    paginate_by = 12 
     
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.values_list('categoria', flat=True).distinct()        
        return queryset 

class ProductoDetailView(DetailView):
    model = Producto
    template_name = "Pape/producto.html"

class CategoriaListView(ListView):
    model = Producto
    template_name = "Pape/categorias.html"
    paginate_by = 12
    
    def get_queryset(self):
        categoria = self.kwargs['categoria'] # obtener la categoría de la URL
        queryset = Producto.objects.filter(categoria=categoria)
        return queryset


class OrdenResumenView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):

        try:
            orden = Orden.objects.get(usuario=self.request.user, ordenado=False)            
            context = { "object":orden }
            return render(self.request, "Pape/orden_resumen.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "No tienes una orden en este momento.")
            return redirect("/")
   

@login_required()
def agregar_carrito(request, slug): #Necesita el slug para saber que prodcuto es el que se agrega al carrito.
    producto = get_object_or_404(Producto, slug=slug) #Se consulta la tabla Producto, y el slug se paso por parametro.
    producto_ordenado, producto_creado = Producto_Ordenado.objects.get_or_create(
        producto=producto,
        usuario=request.user, 
        ordenado=False
        ) #Se crea en la tabla producto ordenado ese producto seleccionado.
    orden_existe = Orden.objects.filter(usuario=request.user, ordenado=False) #Si filtra la tabla orden, buscando ordenes de este usuario sin haber sido enviadas.
    if orden_existe.exists(): #Si existe.
        orden = orden_existe[0] #Se atrapa en esta variable el primer elemento del vector.and
        #Revisamos si el prodcuto ordenado esta dentro de la orden.
        #Aquí hay que comprender la sintaxis del orm de django. 
        #Por ejemplo orden.productos.filter : esta filtrando la tabla de Prodcutos, pero se escirbe con minusculas.
        #producto__slug : tambien esta filtrando la tabal Producto con doble guion bajo.
        if orden.productos.filter(producto__slug=producto.slug).exists():            
            producto_ordenado.cantidad += 1 
            producto_ordenado.save()
            messages.info(request, "Este artículo incremento su cantidad.")
            return redirect("orden_resumen")
        else:
            orden.productos.add(producto_ordenado) 
            messages.info(request, "Este artículo ha sido agregado al carrito.")
            return redirect("orden_resumen")
    #Si el prodcuto no se encuentre dentro  de la orden. 
    else:
        fecha_orden = timezone.now()
        orden = Orden.objects.create(usuario=request.user, fecha_orden=fecha_orden)
        #En la sintaxis delorm, aqui esta filtrando la Tabla Orden, luego su propiedad prodcutos le agrega el prodcuto.
        orden.productos.add(producto_ordenado)
        messages.info(request, "Este artículo ha sido agregado al carrito.")
        return redirect("orden_resumen")
    

@login_required()
def remover_carrito(request, slug):
    producto = get_object_or_404(Producto, slug=slug)    
    orden_existe = Orden.objects.filter(usuario=request.user, ordenado=False)     
    if orden_existe.exists(): 
        orden = orden_existe[0]        
        if orden.productos.filter(producto__slug=producto.slug).exists():
            producto_ordenado = Producto_Ordenado.objects.filter(
                producto = producto,
                usuario = request.user, 
                ordenado = False
            )[0]            
            orden.productos.remove(producto_ordenado)
            messages.info(request, "Este artículo ha sido removido del carrito.")
            return redirect("orden_resumen")
        else:
            messages.info(request, "Este artículo no esta en el carrito.")
            return redirect("producto", slug=slug)
    else:
        messages.info(request, "No hay una orden abierta.")
        return redirect("producto", slug=slug)
    

@login_required()
def reducir_carrito(request, slug):
    producto = get_object_or_404(Producto, slug=slug)    
    orden_existe = Orden.objects.filter(usuario=request.user, ordenado=False)     
    if orden_existe.exists(): 
        orden = orden_existe[0]        
        if orden.productos.filter(producto__slug=producto.slug).exists():
            producto_ordenado = Producto_Ordenado.objects.filter(
                producto = producto,
                usuario = request.user, 
                ordenado = False
            )[0]            
            if  producto_ordenado.cantidad > 1:
                producto_ordenado.cantidad -= 1
                producto_ordenado.save()
            else:
                orden.productos.remove(producto_ordenado)
            messages.info(request, "Se ha reducido la cantidad de artículos.")
            return redirect("orden_resumen")
        else:
            messages.info(request, "Este artículo no esta en el carrito.")
            return redirect("producto", slug=slug)
    else:
        messages.info(request, "No hay una orden abierta.")
        return redirect("producto", slug=slug)


def buscar(request):
    nombre = request.GET.get('buscar')
    context = {
        'productos' : Producto.objects.filter(nombre__icontains=nombre)
    }    
    return render(request, 'Pape/buscar.html', context)

def about(request):
    return render(request, 'Pape/about.html', {'title': 'About'})

