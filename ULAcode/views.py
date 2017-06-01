from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Usuario, Framework, RolUsuario
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin


from .forms import RegisterForm, UpdateProfileForm, FrameworkUpdateForm, FrameworkCreateForm

# Vistas que no requieren estar autenticado
class AcercaDe(View):
    def get(self, request):
        return render(request, 'ULAcode/acerca_de.html')


class Index(View):
    def get(self, request):
        return render(request, 'ULAcode/index.html')


class Registro(View):
    """Clase que maneja el Registro de un Usuario."""

    def get(self, request):
        """Funcion que responde a la Solicitud HTTP GET de la url asignada a esta vista."""
        form = RegisterForm
        return render(request, 'ULAcode/registro_boots.html', {'form': form})

    def post(self, request):
        """Funcion que responde a la Solicitud HTTP POST de la url asignada a esta vista."""
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = Usuario()
            # return HttpResponse(usuario.fotoPerfil.name)
            framework = Framework()
            framework.urlFramework = form.cleaned_data['urlFramework']
            framework.frameworkToken = form.cleaned_data['frameworkToken']
            user = form.save()
            framework.emailAdminFramework = user.email
            framework.save()
            usuario.cedula = form.cleaned_data['cedula']
            usuario.fotoAuth = request.FILES['foto_auth']
            usuario.fotoPerfil = request.FILES['foto_perfil']
            usuario.fotoPerfil.name = usuario.cedula + "_" + usuario.fotoPerfil.name
            usuario.fotoAuth.name = usuario.cedula + "_" + usuario.fotoAuth.name
            rolUsuario = form.cleaned_data['rolUsuario']
            user.username = user.email
            user.is_active = 0
            user.save()
            usuario.relUser = user
            usuario.save()
            for rol in rolUsuario:
                usuario.userRol.add(rol)
                if rol == '1':
                    user.groups.add(1)
                elif rol == '2':
                    user.groups.add(2)
                else:
                    user.groups.add(3)
            usuario.userToFramework.add(framework)
            return HttpResponseRedirect(reverse('index'))


# Vistas que requieren autenticacion
# Vistas de Perfil Propio
class Perfil(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        userData = User.objects.get(id=request.user.id)
        usuario = Usuario.objects.get(relUser_id=request.user.id)
        rolUser = RolUsuario.objects.filter(usuario__cedula=usuario.cedula).values('id')
        framework = Framework.objects.filter(usuario__cedula=usuario.cedula).values('urlFramework')
        return render(request, 'ULAcode/profile.html', {'userData': userData, 'usuario': usuario, 'rolUser': rolUser, 'framework': framework})


class UpdatePerfil(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        userData = User.objects.get(id=request.user.id)
        usuario = Usuario.objects.get(relUser_id=request.user.id)
        rolUser = RolUsuario.objects.filter(usuario__cedula__exact=usuario.cedula).values('id')
        rolUsuario = list()
        for rol in rolUser:
            rolUsuario.append(rol['id'])
        data = {
            'first_name': userData.first_name,
            'last_name': userData.last_name,
            'email': userData.email,
            'cedula': usuario.cedula,
            'rolUsuario': rolUsuario,
        }
        form = UpdateProfileForm(initial=data)
        return render(request, 'ULAcode/editar_perfil.html', {'form': form})

    def post(self, request):
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            user = User()
            user = User.objects.get(id=request.user.id)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.username = user.email
            user.save()
            usuario = Usuario.objects.get(relUser=user)
            usuario.cedula = form.cleaned_data['cedula']
            rolUsuario = form.cleaned_data['rolUsuario']
            usuario.save()
            usuario.userRol.clear()
            user.groups.clear()
            for rol in rolUsuario:
                usuario.userRol.add(rol)
                if rol == '1':
                    user.groups.add(1)
                elif rol == '2':
                    user.groups.add(2)
                else:
                    user.groups.add(3)
            # user.is_active???
            return HttpResponseRedirect(reverse('logout'))


# Vistas de administracion de Usuarios, solo accesible por Administradores de Sistemas
class UserList(PermissionRequiredMixin, AccessMixin, ListView):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'auth.change_user'
    model = User
    template_name = 'ULAcode/user_list.html'

    def get_context_data(self, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        context['usuarios'] = Usuario.objects.all()
        return context


class UserProfile(PermissionRequiredMixin, AccessMixin, View):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'auth.change_user'

    def get(self, request, userId):
        userData = User.objects.get(id=userId)
        usuario = Usuario.objects.get(relUser_id=userId)
        rolUser = RolUsuario.objects.filter(usuario__cedula__exact=usuario.cedula).values('id')
        framework = Framework.objects.filter(usuario__cedula__exact=usuario.cedula).values()
        return render(request, 'ULAcode/user_profile.html', {'userData': userData, 'usuario': usuario, 'rolUser': rolUser, 'framework': framework})


class UpdateUser(PermissionRequiredMixin, AccessMixin, View):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'auth.change_user'

    def get(self, request, userId):
        userData = User.objects.get(id=userId)
        usuario = Usuario.objects.get(relUser_id=userId)
        rolUser = RolUsuario.objects.filter(usuario__cedula__exact=usuario.cedula).values('id')
        rolUsuario = list()
        for rol in rolUser:
            rolUsuario.append(rol['id'])
        data = {
            'first_name': userData.first_name,
            'last_name': userData.last_name,
            'email': userData.email,
            'cedula': usuario.cedula,
            'rolUsuario': rolUsuario,
            }
        form = UpdateProfileForm(initial=data)
        return render(request, 'ULAcode/editar_usuario.html', {'form': form})

    def post(self, request, userId):
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            user = User()
            user = User.objects.get(id=userId)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.username = user.email
            # user.is_active = False
            user.save()
            usuario = Usuario.objects.get(relUser=user)
            usuario.cedula = form.cleaned_data['cedula']
            rolUsuario = form.cleaned_data['rolUsuario']
            usuario.save()
            usuario.userRol.clear()
            user.groups.clear()
            for rol in rolUsuario:
                usuario.userRol.add(rol)
                if rol == '1':
                    user.groups.add(1)
                elif rol == '2':
                    user.groups.add(2)
                else:
                    user.groups.add(3)
            return HttpResponseRedirect(reverse('user_list'))


class CrearUsuario(PermissionRequiredMixin, AccessMixin, View):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'auth.add_user'

    def get(self, request):
        form = RegisterForm
        return render(request, 'ULAcode/crear_usuario.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = Usuario()
            framework = Framework()
            framework.urlFramework = form.cleaned_data['urlFramework']
            framework.frameworkToken = form.cleaned_data['frameworkToken']
            user = form.save()
            framework.emailAdminFramework = user.email
            framework.save()
            usuario.cedula = form.cleaned_data['cedula']
            usuario.fotoAuth = request.FILES['foto_auth']
            usuario.fotoPerfil = request.FILES['foto_perfil']
            usuario.fotoPerfil.name = usuario.cedula + "_" + usuario.fotoPerfil.name
            usuario.fotoAuth.name = usuario.cedula + "_" + usuario.fotoAuth.name
            rolUsuario = form.cleaned_data['rolUsuario']
            user.username = user.email
            user.is_active = 0
            user.save()
            usuario.relUser = user
            usuario.save()
            for rol in rolUsuario:
                usuario.userRol.add(rol)
                if rol == '1':
                    user.groups.add(1)
                elif rol == '2':
                    user.groups.add(2)
                else:
                    user.groups.add(3)
            usuario.userToFramework.add(framework)
            usuario.userToFramework.add(framework)
            return HttpResponseRedirect(reverse('user_list'))


class ActivarDesactivarUsuario(PermissionRequiredMixin, AccessMixin, View):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'auth.change_user'


    def get(self, request, userId):
        user = User.objects.get(id=userId)
        if user.is_active is False:
            user.is_active = True
        else:
            user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('user_list'))


class ActivarUsuario(PermissionRequiredMixin, AccessMixin, View):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'auth.change_user'

    def get(self, request, userId):
        user = User.objects.get(id=userId)
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('user_profile', args=(userId,)))


class DesactivarUsuario(PermissionRequiredMixin, AccessMixin, View):
    """."""
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'auth.change_user'

    def get(self, request, userId):
        user = User.objects.get(id=userId)
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('user_profile', args=(userId,)))


# Vistas de Administracion de Frameworks(Administrador de Sistema)
class FrameworkList(PermissionRequiredMixin, AccessMixin, ListView):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'ULAcode.delete_framework'

    model = Framework
    template_name = 'ULAcode/frameworks_list.html'


class FrameworkDetail(PermissionRequiredMixin, AccessMixin, DetailView):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'ULAcode.delete_framework'

    model = Framework
    template_name = 'ULAcode/framework_detail.html'


class ActivarDesactivarFramework(PermissionRequiredMixin, AccessMixin, View):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'ULAcode.delete_framework'
    def get(self, request, urlFramework):
        framework = Framework.objects.get(urlFramework=urlFramework)
        if framework.frameworkActivo is False:
            framework.frameworkActivo = True
        else:
            framework.frameworkActivo = False
        framework.save()
        return HttpResponseRedirect(reverse('framework_list'))


class UpdateFramework(PermissionRequiredMixin, AccessMixin, View):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'ULAcode.delete_framework'
    def get(self, request, urlFramework):
        framework = Framework.objects.get(urlFramework=urlFramework)
        data = {
            'urlFramework': framework.urlFramework,
            'frameworkToken': framework.frameworkToken,
            }
        form = FrameworkUpdateForm(initial=data)
        return render(request, 'ULAcode/framework_form.html', {'form': form})

    def post(self, request, urlFramework):
        form = FrameworkUpdateForm(request.POST)
        if form.is_valid():
            framework = Framework.objects.get(urlFramework=urlFramework)
            usuariosFramework = framework.usuario_set.all()
            for usuario in usuariosFramework:
                usuario.userToFramework.remove(framework)
            framework.delete()
            framework.urlFramework = form.cleaned_data['urlFramework']
            framework.frameworkToken = form.cleaned_data['frameworkToken']
            framework.frameworkActivo = False
            framework.save()
            for usuario in usuariosFramework:
                usuario.userToFramework.add(framework)
            return HttpResponseRedirect(reverse('framework_list'))


class ActivarFramework(PermissionRequiredMixin, AccessMixin, View):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'ULAcode.delete_framework'
    def get(self, request, urlFramework):
        framework = Framework.objects.get(urlFramework=urlFramework)
        framework.frameworkActivo = True
        framework.save()
        return HttpResponseRedirect(reverse('framework_detail', args=(urlFramework,)))


class DesactivarFramework(PermissionRequiredMixin, AccessMixin, View):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'framework.delete_framework'
    def get(self, request, urlFramework):
        framework = Framework.objects.get(urlFramework=urlFramework)
        framework.frameworkActivo = False
        framework.save()
        return HttpResponseRedirect(reverse('framework_detail', args=(urlFramework,)))


# Creacion de Framework Nuevo(Administrador de Sistema y Administrador de Framework)
class CreateFramework(PermissionRequiredMixin, AccessMixin, View):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'ULAcode.add_framework'
    def get(self, request):
        form = FrameworkCreateForm()
        return render(request, 'ULAcode/framework_form.html', {'form': form})

    def post(self, request):
        form = FrameworkCreateForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            framework = Framework()
            framework.urlFramework = form.cleaned_data['urlFramework']
            framework.frameworkToken = form.cleaned_data['frameworkToken']
            framework.frameworkActivo = False
            framework.emailAdminFramework = user.email
            framework.save()
            return HttpResponseRedirect(reverse('framework_list'))


class UpdateRelatedFramework(PermissionRequiredMixin, AccessMixin, View):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'ULAcode.change_related_framework'

    def get(self, request, urlFramework):
        user = User.objects.get(id=request.user.id)
        framework = Framework.objects.get(urlFramework=urlFramework)
        if user.email != framework.emailAdminFramework:
            return HttpResponseForbidden("Usted no es administrador de este Framework")
        data = {
            'urlFramework': framework.urlFramework,
            'frameworkToken': framework.frameworkToken,
            }
        form = FrameworkUpdateForm(initial=data)
        return render(request, 'ULAcode/framework_form.html', {'form': form})

    def post(self, request, urlFramework):
        form = FrameworkUpdateForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            framework = Framework.objects.get(urlFramework=urlFramework)
            if user.email != framework.emailAdminFramework:
                return HttpResponseForbidden("Usted no es administrador de este Framework")
            usuariosFramework = framework.usuario_set.all()
            for usuario in usuariosFramework:
                usuario.userToFramework.remove(framework)
            framework.delete()
            framework.urlFramework = form.cleaned_data['urlFramework']
            framework.frameworkToken = form.cleaned_data['frameworkToken']
            framework.frameworkActivo = False
            framework.save()
            for usuario in usuariosFramework:
                usuario.userToFramework.add(framework)
            return HttpResponseRedirect(reverse('related_frameworks_admin'))


class RelatedFrameworksAdminList(PermissionRequiredMixin, AccessMixin, View):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'ULAcode.change_related_framework'
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        frameworks = Framework.objects.filter(emailAdminFramework=user.email).values('urlFramework')
        return render(request, "ULAcode/related_frameworks_admin.html", {'frameworks': frameworks})


# Listar los Frameworks Relacionados Administrador de Framework y Usuario Comun
class RelatedFrameworksList(PermissionRequiredMixin, AccessMixin, View):
    raise_exception = True
    permission_denied_message = "No cuenta con los permisos necesarios para acceder esta pagina"
    permission_required = 'ULAcode.list_related_frameworks'
    def get(self, request):
        usuario = Usuario.objects.get(relUser=request.user.id)
        frameworks = Framework.objects.filter(usuario__cedula=usuario.cedula).values('urlFramework')
        return render(request, "ULAcode/related_frameworks.html", {'frameworks': frameworks})
