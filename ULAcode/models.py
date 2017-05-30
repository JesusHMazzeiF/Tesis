from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RolUsuario(models.Model):
	rol = models.CharField("Rol del Usuario",unique=True, max_length=15)

class Framework(models.Model):
	urlFramework = models.CharField("URL del Framework",max_length=50, unique=True, primary_key=True)
	frameworkActivo = models.BooleanField(default=False)
	frameworkToken = models.CharField("Token del API externa",max_length=256)



class Usuario(models.Model):
	relUser = models.OneToOneField(User, on_delete=models.CASCADE)
	cedula = models.CharField("Cedula del Usuario",max_length=10, primary_key=True)
	fotoPerfil = models.ImageField("Foto de Perfil",upload_to='perfilUsuarios')
	fotoAuth = models.ImageField("Foto para Autenticacion",upload_to='authUsuario')
	userRol = models.ManyToManyField(RolUsuario)
	userToFramework = models.ManyToManyField(Framework)
