"""ulacode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from ULAcode import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.Registro.as_view(), name='registroUsuario'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^acercaDe/$', views.AcercaDe.as_view(), name='acerca_de'),
    url(r'^profile/$', views.Perfil.as_view(), name='perfil'),
    url(r'^activar/(?P<userId>[0-9]*)$', views.ActivarUsuario.as_view(), name = 'activarUsuario'),
    url(r'^editarPerfil/$', views.UpdatePerfil.as_view(), name = 'editarPerfil'),
    url(r'^userList/$', views.UserList.as_view(), name = 'userList'),
    url(r'^userList/(?P<userId>[0-9]*)$', views.UserProfile.as_view(), name = 'userProfile'),
    url(r'^editarUsuario/(?P<userId>[0-9]*)$', views.UpdateUser.as_view(), name = 'editarUsuario'),
    url(r'^crearUsuario/', views.CrearUsuario.as_view(), name = 'crearUsuario')

]
