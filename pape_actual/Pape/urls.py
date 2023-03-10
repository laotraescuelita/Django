from django.urls import path 
from .views import (     
    about,    
    ProductoDetailView,
    InicioView,
    agregar_carrito,
    remover_carrito,
    OrdenResumenView,
    reducir_carrito,
    buscar,
    CategoriaListView, 
    datos_productos
    )


urlpatterns = [
    path("", InicioView.as_view(), name="inicio"),    
    path("producto/<slug:slug>/", ProductoDetailView.as_view(), name="producto"),    
    path("agregar_carrito/<slug:slug>/", agregar_carrito, name="agregar_carrito"),
    path("remover_carrito/<slug:slug>/", remover_carrito, name="remover_carrito"),
    path("orden_resumen/", OrdenResumenView.as_view(), name="orden_resumen"),
    path("reducir_carrito/<slug:slug>/", reducir_carrito, name="reducir_carrito"),
    path("buscar/", buscar, name="buscar"),
    path("categorias/<str:categoria>/", CategoriaListView.as_view(), name="categorias"),
    path("datos/", datos_productos, name="datos")
    
]
