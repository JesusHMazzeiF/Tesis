from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import View
from .models import Usuario, Framework, RolUsuario
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.urls import reverse

from .forms import RegisterForm, UpdateProfileForm, FrameworkUpdateForm, FrameworkCreateForm


class Registro(View):
    """Clase que maneja el Registro de un Usuario."""

    def get(self, request):
        """Funcion que responde a la Solicitud HTTP GET de la url asignada a esta vista."""
        form = RegisterForm
        return render(request, 'ULAcode/crear_usuario.html', {'form': form})

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


class AcercaDe(View):
    def get(self, request):
        return render(request, 'ULAcode/acerca_de.html')


class Perfil(View):
    def get(self, request):
        userData = User.objects.get(id=request.user.id)
        usuario = Usuario.objects.get(relUser_id=request.user.id)
        rolUser = RolUsuario.objects.filter(usuario__cedula=usuario.cedula).values('id')
        framework = Framework.objects.filter(usuario__cedula=usuario.cedula).values('urlFramework')
        return render(request, 'ULAcode/profile.html', {'userData': userData, 'usuario': usuario, 'rolUser': rolUser, 'framework': framework})


def index(request):
    return render(request, 'ULAcode/index.html')


class UserList(ListView):
    model = User
    template_name = 'ULAcode/user_list.html'

    def get_context_data(self, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        context['usuarios'] = Usuario.objects.all()
        return context


class UserProfile(View):
    def get(self, request, userId):
        userData = User.objects.filter(id=userId).values('id', 'first_name', 'last_name', 'email', 'is_active')
        usuario = Usuario.objects.filter(relUser_id=userId).values()
        rolUser = RolUsuario.objects.filter(usuario__cedula__exact=usuario[0]['cedula']).values()
        framework = Framework.objects.filter(usuario__cedula__exact=usuario[0]['cedula']).values()
        return render(request, 'ULAcode/user_profile.html', {'userData': userData, 'usuario': usuario, 'rolUser': rolUser, 'framework': framework})


class ActivarDesactivarUsuario(View):
    def get(self, request, userId):
        user = User.objects.get(id=userId)
        if user.is_active is False:
            user.is_active = True
        else:
            user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('user_list'))


class ActivarUsuario(View):
    def get(self, request, userId):
        user = User.objects.get(id=userId)
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('user_profile', args=(userId,)))


class DesactivarUsuario(View):
    """."""

    def get(self, request, userId):
        user = User.objects.get(id=userId)
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('user_profile', args=(userId,)))


class UpdatePerfil(View):
    def get(self, request):
        userData = User.objects.filter(id=request.user.id).values('first_name', 'last_name', 'email')
        usuario = Usuario.objects.filter(relUser_id=request.user.id).values()
        rolUser = RolUsuario.objects.filter(usuario__cedula__exact=usuario[0]['cedula']).values('id')
        rolUsuario = list()
        for rol in rolUser:
            rolUsuario.append(rol['id'])
        data = {
            'first_name': userData[0]['first_name'],
            'last_name': userData[0]['last_name'],
            'email': userData[0]['email'],
            'cedula': usuario[0]['cedula'],
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
            usuario = Usuario()
            usuario.cedula = form.cleaned_data['cedula']
            rolUsuario = form.cleaned_data['rolUsuario']
            user.save()
            usuario.relUser = user
            usuario.save()
            usuario.userRol.clear()
            for rol in rolUsuario:
                usuario.userRol.add(rol)
            return HttpResponseRedirect(reverse('logout'))


class UpdateUser(View):
    def get(self, request, userId):
        userData = User.objects.filter(id=userId).values('first_name', 'last_name', 'email')
        usuario = Usuario.objects.filter(relUser_id=userId).values()
        rolUser = RolUsuario.objects.filter(usuario__cedula__exact=usuario[0]['cedula']).values('id')
        framework = Framework.objects.filter(usuario__cedula__exact=usuario[0]['cedula']).values()
        rolUsuario = list()
        for rol in rolUser:
            rolUsuario.append(rol['id'])
        data = {
            'first_name': userData[0]['first_name'],
            'last_name': userData[0]['last_name'],
            'email': userData[0]['email'],
            'cedula': usuario[0]['cedula'],
            'rolUsuario': rolUsuario,
            }
        form = UpdateProfileForm(initial=data)
        return render(request, 'ULAcode/editar_perfil.html', {'form': form})

    def post(self, request, userId):
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            user = User()
            user = User.objects.get(id=userId)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.username = user.email
            usuario = Usuario()
            usuario.cedula = form.cleaned_data['cedula']
            rolUsuario = form.cleaned_data['rolUsuario']
            # user.is_active = False
            user.save()
            usuario.relUser = user
            usuario.save()
            usuario.userRol.clear()
            for rol in rolUsuario:
                usuario.userRol.add(rol)
            return HttpResponseRedirect(reverse('user_list'))


class CrearUsuario(View):
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


class FrameworkList(ListView):
    model = Framework
    template_name = 'ULAcode/frameworks_list.html'


class FrameworkDetail(DetailView):
    model = Framework
    template_name = 'ULAcode/framework_detail.html'


class ActivarDesactivarFramework(View):
    def get(self, request, urlFramework):
        framework = Framework.objects.get(urlFramework=urlFramework)
        if framework.frameworkActivo is False:
            framework.frameworkActivo = True
        else:
            framework.frameworkActivo = False
        framework.save()
        return HttpResponseRedirect(reverse('framework_list'))


class UpdateFramework(View):
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


class CreateFramework(View):
    def get(self, request):
        form = FrameworkCreateForm()
        return render(request, 'ULAcode/framework_form.html', {'form': form})

    def post(self, request):
        form = FrameworkCreateForm(request.POST)
        if form.is_valid():
            framework = Framework()
            framework.urlFramework = form.cleaned_data['urlFramework']
            framework.frameworkToken = form.cleaned_data['frameworkToken']
            framework.frameworkActivo = False
            framework.save()
            return HttpResponseRedirect(reverse('framework_list'))


class RelatedFrameworks(View):
    def get(self, request):
        usuario = Usuario.objects.get(relUser=request.user.id)
        frameworks = Framework.objects.filter(usuario__cedula=usuario.cedula)
        return HttpResponse("ULAcode/related_frameworks.html", {framewo})


class ActivarFramework(View):
    def get(self, request, urlFramework):
        framework = Framework.objects.get(urlFramework=urlFramework)
        framework.frameworkActivo = True
        framework.save()
        return HttpResponseRedirect(reverse('framework_detail', args=(urlFramework,)))


class DesactivarFramework(View):
    def get(self, request, urlFramework):
        framework = Framework.objects.get(urlFramework=urlFramework)
        framework.frameworkActivo = False
        framework.save()
        return HttpResponseRedirect(reverse('framework_detail', args=(urlFramework,)))
