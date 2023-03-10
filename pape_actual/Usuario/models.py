from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(default='usuario.jpg', upload_to='img_perfil')

    def __str__(self):
        return f'{self.usuario.username} Perfil'

    def save(self):
        super().save()

        img = Image.open(self.imagen.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.imagen.path)