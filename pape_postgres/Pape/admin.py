from django.contrib import admin
from .models import ( 
    Producto,
    Producto_Ordenado, 
    Orden
)

admin.site.register( Producto )
admin.site.register( Producto_Ordenado )
admin.site.register( Orden )

