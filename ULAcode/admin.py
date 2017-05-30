from django.contrib import admin

# Register your models here.
from .models import Usuario, RolUsuario, Framework

admin.site.register(Usuario)
admin.site.register(RolUsuario)
admin.site.register(Framework)