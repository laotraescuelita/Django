from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import Forma_Registro, Forma_Actualizar_Usuario, Forma_Actualizar_Perfil

def registrarse(request):
    if request.method == 'POST':
        forma = Forma_Registro(request.POST)
        if forma.is_valid():
            forma.save()
            usuario = forma.cleaned_data.get('username')
            messages.success(request, f'Tu cuenta ha sido creada! Ahora puedes ingresar.')
            return redirect('ingresar')
    else:
        forma = Forma_Registro()
    return render(request, 'Usuario/registro.html', {'forma': forma} )

@login_required
def perfil(request):
    if request.method == 'POST':
        u_forma = Forma_Actualizar_Usuario(request.POST, instance=request.user)
        p_forma = Forma_Actualizar_Perfil(request.POST,
                                   request.FILES,
                                   instance=request.user.perfil)
        if u_forma.is_valid() and p_forma.is_valid():
            u_forma.save()
            p_forma.save()
            messages.success(request, f'Tu cuenta ha sido actualizada!')
            return redirect('perfil')
    else:
        u_forma = Forma_Actualizar_Usuario(instance=request.user)
        p_forma = Forma_Actualizar_Perfil(instance=request.user.perfil)

    context = {
        'u_forma': u_forma,
        'p_forma': p_forma
    }
    
    return render(request, "Usuario/perfil.html", context)
    
