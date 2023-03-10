from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

class Forma_Registro(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class Forma_Actualizar_Usuario(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class Forma_Actualizar_Perfil(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen']
