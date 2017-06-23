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
from django.conf.urls.static import static
from django.conf import settings

from ULAcode import views
from ULAcode.forms import CustomLoginForm

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^register/$', views.Registro.as_view(), name='registro_usuario'),
    url(r'^login/$', auth_views.LoginView.as_view(), {'form': CustomLoginForm}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(), {'success_url': 'logout/'}, name='password_change'),
    url(r'^acerca_de/$', views.AcercaDe.as_view(), name='acerca_de'),
    url(r'^profile/$', views.Perfil.as_view(), name='perfil'),
    url(r'^activar/(?P<userId>[0-9]*)$', views.ActivarUsuario.as_view(), name='activar_usuario'),
    url(r'^desactivar/(?P<userId>[0-9]*)$', views.DesactivarUsuario.as_view(), name='desactivar_usuario'),
    url(r'^editar_perfil/$', views.UpdatePerfil.as_view(), name='editar_perfil'),
    url(r'^user_list/$', views.UserList.as_view(), name='user_list'),
    url(r'^user_list/(?P<userId>[0-9]*)$', views.UserProfile.as_view(), name='user_profile'),
    url(r'^editar_usuario/(?P<userId>[0-9]*)$', views.UpdateUser.as_view(), name='editar_usuario'),
    url(r'^crear_usuario/', views.CrearUsuario.as_view(), name='crear_usuario'),
    url(r'^framework_list/(?P<urlFramework>[\w\/-]+)$', views.ActivarDesactivarFramework.as_view(), name='framework_info'),
    url(r'^framework_list/$', views.FrameworkList.as_view(), name='framework_list'),
    url(r'^user_list/control/(?P<userId>[0-9]*)$', views.ActivarDesactivarUsuario.as_view(), name='user_info'),
    url(r'^framework_update/(?P<urlFramework>[\w\/-]+)$', views.UpdateFramework.as_view(), name='framework_update'),
    url(r'^framework_create/$', views.CreateFramework.as_view(), name='framework_create'),
    url(r'^related_frameworks/$', views.RelatedFrameworksList.as_view(), name='related_frameworks'),
    url(r'^framework_detail/-(?P<pk>[\w\/-]+)$', views.FrameworkDetail.as_view(), name="framework_detail"),
    url(r'^activar_framework/-(?P<urlFramework>[\w\/-]+)$', views.ActivarFramework.as_view(), name='activar_framework'),
    url(r'^desactivar_framework/-(?P<urlFramework>[\w\/-]+)$', views.DesactivarFramework.as_view(), name='desactivar_framework'),
    url(r'^related_frameworks_admin/$', views.RelatedFrameworksAdminList.as_view(), name='related_frameworks_admin'),
    url(r'^related_frameworks_admin/-(?P<urlFramework>[\w\/-]+)$', views.UpdateRelatedFramework.as_view(), name='update_related_framework'),

]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
