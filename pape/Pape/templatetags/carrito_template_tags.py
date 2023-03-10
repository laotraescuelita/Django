from django import template
from Pape.models import Orden 

register = template.Library()

@register.filter
def cuenta_articulos_carrito(user):
    if user.is_authenticated:
        qs = Orden.objects.filter(usuario=user, ordenado=False)
        if qs.exists():
            return qs[0].productos.count()
    return 0 
