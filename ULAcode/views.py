from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import View
from .models import Usuario, Framework, RolUsuario
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.urls import reverse

from .forms import RegisterForm, UpdateProfileForm, UpdateUserForm, FrameworkUpdateForm, FrameworkCreateForm

class Registro(View):
	def get(self, request):
		form = RegisterForm
		return render(request,'ULAcode/name.html', {'form': form})

	def post(self, request):
		form = RegisterForm(request.POST, request.FILES)
		if form.is_valid():
			usuario = Usuario()
			framework = Framework()
			framework.urlFramework = form.cleaned_data['urlFramework']
			framework.frameworkToken = form.cleaned_data['frameworkToken']
			framework.save()
			usuario.cedula = form.cleaned_data['cedula']
			usuario.fotoAuth = request.FILES['foto_auth']
			usuario.fotoPerfil = request.FILES['foto_perfil']
			rolUsuario = form.cleaned_data['rolUsuario']
			user  = form.save()
			user.username = user.email
			user.is_active = 0
			user.save()
			usuario.relUser = user
			usuario.save()
			for rol in rolUsuario:
				usuario.userRol.add(rol)
			usuario.userToFramework.add(framework)
			return HttpResponseRedirect(reverse('index'))

class AcercaDe(View):
	def get(self, request):
		return render(request, 'ULAcode/acerca_de.html')

class Perfil(View):
	def get(self, request):
		userData = User.objects.filter(id = request.user.id).values('first_name', 'last_name', 'email')
		usuario = Usuario.objects.filter(relUser_id = request.user.id).values()
		rolUser = RolUsuario.objects.filter(usuario__cedula__exact=usuario[0]['cedula']).values()
		framework = Framework.objects.filter(usuario__cedula__exact=usuario[0]['cedula']).values()
		return render(request, 'ULAcode/profile.html', { 'userData' : userData ,'usuario' : usuario , 'rolUser' : rolUser, 'framework': framework})

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
		userData = User.objects.filter(id = userId).values('id', 'first_name', 'last_name', 'email', 'is_active')
		usuario = Usuario.objects.filter(relUser_id = userId ).values()
		rolUser = RolUsuario.objects.filter(usuario__cedula__exact=usuario[0]['cedula']).values()
		framework = Framework.objects.filter(usuario__cedula__exact=usuario[0]['cedula']).values()
		return render(request, 'ULAcode/user_profile.html', { 'userData' : userData ,'usuario' : usuario , 'rolUser' : rolUser, 'framework': framework})

class ActivarDesactivarUsuario(View):
	def get(self, request, userId):
		user = User.objects.get(id = userId)
		if user.is_active == False:
			user.is_active = True
		else:
			user.is_active = False
		user.save()
		return HttpResponseRedirect(reverse('userList'))

class ActivarUsuario(View):
	def get(self, request, userId):
		user = User.objects.get(id = userId)
		user.is_active = True
		user.save()
		return HttpResponseRedirect(reverse('userProfile', args=(userId,)))

class DesactivarUsuario(View):
	def get(self, request, userId):
		user = User.objects.get(id = userId)
		user.is_active = False
		user.save()
		return HttpResponseRedirect(reverse('userProfile', args=(userId,)))

class UpdatePerfil(View):
	def get(self, request):
		userData = User.objects.filter(id = request.user.id).values('first_name', 'last_name', 'email')
		usuario = Usuario.objects.filter(relUser_id = request.user.id).values()
		rolUser = RolUsuario.objects.filter(usuario__cedula__exact=usuario[0]['cedula']).values('id')
		rolUsuario = list()
		for rol in rolUser:
			rolUsuario.append(rol['id'])
		data = {
			'first_name' : userData[0]['first_name'],
			'last_name' : userData[0]['last_name'],
			'email' : userData[0]['email'],
			'cedula' : usuario[0]['cedula'],
			'rolUsuario': rolUsuario,

		}
		form = UpdateProfileForm(initial = data)
		return render(request,'ULAcode/editPerfil.html', {'form': form})


	def post(self, request):
		form = UpdateProfileForm(request.POST)
		if form.is_valid():
			user = User()
			user = User.objects.get(id = request.user.id)
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
		userData = User.objects.filter(id = userId).values('first_name', 'last_name', 'email')
		usuario = Usuario.objects.filter(relUser_id = userId).values()
		rolUser = RolUsuario.objects.filter(usuario__cedula__exact=usuario[0]['cedula']).values('id')
		framework = Framework.objects.filter(usuario__cedula__exact=usuario[0]['cedula']).values()
		rolUsuario = list()
		for rol in rolUser:
			rolUsuario.append(rol['id'])
		data = {
			'first_name' : userData[0]['first_name'],
			'last_name' : userData[0]['last_name'],
			'email' : userData[0]['email'],
			'cedula' : usuario[0]['cedula'],
			'rolUsuario': rolUsuario,

		}
		form = UpdateProfileForm(initial = data)
		return render(request,'ULAcode/editPerfil.html', {'form': form})


	def post(self, request, userId):
		form = UpdateProfileForm(request.POST)
		if form.is_valid():
			user = User()
			user = User.objects.get(id = userId)
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.email = form.cleaned_data['email']
			user.username = user.email
			usuario = Usuario()
			usuario.cedula = form.cleaned_data['cedula']
			rolUsuario = form.cleaned_data['rolUsuario']
			#user.is_active = False
			user.save()
			usuario.relUser = user
			usuario.save()
			usuario.userRol.clear()
			for rol in rolUsuario:
				usuario.userRol.add(rol)
			return HttpResponseRedirect(reverse('userList'))


class CrearUsuario(View):
	def get(self, request):
		form = RegisterForm
		return render(request,'ULAcode/name.html', {'form': form})

	def post(self, request):
		form = RegisterForm(request.POST, request.FILES)
		if form.is_valid():
			usuario = Usuario()
			framework = Framework()
			framework.urlFramework = form.cleaned_data['urlFramework']
			framework.frameworkToken = form.cleaned_data['frameworkToken']
			framework.save()
			usuario.cedula = form.cleaned_data['cedula']
			usuario.fotoAuth = request.FILES['foto_auth']
			usuario.fotoPerfil = request.FILES['foto_perfil']
			rolUsuario = form.cleaned_data['rolUsuario']
			user  = form.save()
			user.username = user.email
			user.is_active = 0
			user.save()
			usuario.relUser = user
			usuario.save()
			for rol in rolUsuario:
				usuario.userRol.add(rol)
			usuario.userToFramework.add(framework)
			return HttpResponseRedirect(reverse('perfil'))


class FrameworkList(ListView):
	model = Framework
	template_name = 'ULAcode/frameworks_list.html'

class ActivarDesactivarFramework(View):
	def get(self, request, urlFramework):
		framework = Framework.objects.get(urlFramework = urlFramework)
		if framework.frameworkActivo == False:
			framework.frameworkActivo = True
		else:
			framework.frameworkActivo = False
		framework.save()
		return HttpResponseRedirect(reverse('frameworkList'))

class UpdateFramework(View):
	def get(self, request, urlFramework):
		framework = Framework.objects.get(urlFramework = urlFramework)
		data = {
			'urlFramework' : framework.urlFramework,
			'frameworkToken' : framework.frameworkToken,
		}
		form = FrameworkUpdateForm(initial = data)
		return render(request,'ULAcode/framework_form.html', {'form': form})


	def post(self, request, urlFramework):
		form = FrameworkUpdateForm(request.POST)
		if form.is_valid():
			framework = Framework()
			framework = Framework.objects.get(urlFramework = urlFramework)
			framework.urlFramework = form.cleaned_data['urlFramework']
			framework.frameworkToken = form.cleaned_data['frameworkToken']
			framework.frameworkActivo = False
			framework.save()
			return HttpResponseRedirect(reverse('frameworkList'))


class CreateFramework(View):

	def get(self, request):
		form = FrameworkCreateForm()
		return render(request,'ULAcode/framework_form.html', {'form': form})


	def post(self, request):
		form = FrameworkCreateForm(request.POST)
		if form.is_valid():
			framework = Framework()
			framework.urlFramework = form.cleaned_data['urlFramework']
			framework.frameworkToken = form.cleaned_data['frameworkToken']
			framework.frameworkActivo = False
			framework.save()
			return HttpResponseRedirect(reverse('frameworkList'))
