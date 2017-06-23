from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import re
from .models import Usuario, Framework

cedula_regex = "r'^[vVeE][0-9]{9}'"


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Nombre', max_length='30')
    last_name = forms.CharField(label='Apellido', max_length='30')
    cedula = forms.CharField(label='Cedula', max_length='10',
        validators=
            [RegexValidator(regex=r'^[VvEe][0-9]{9}$',
                message='La cedula debe estar en formato V000000000',
                code='cedula invalida')],
                help_text='Formato V000000000'
        )
    foto_perfil = forms.ImageField(label='Foto Perfil', required=False)
    foto_auth = forms.ImageField(label='Foto para Autenticacion', required=False)
    rolChoices = (
        (3, 'Usuario Comun'),
        (1, 'Administrador de Sistema'),
        (2, 'Administrador de Framework'),
        )
    rolUsuario = forms.MultipleChoiceField(label='Rol del Usuario en el Sistema', choices=rolChoices, widget=forms.CheckboxSelectMultiple, help_text='Los roles que ejercera en el sistema')
    urlFramework = forms.CharField(label="URL del Framework", max_length=50, required=False)
    frameworkToken = forms.CharField(label="Token del API externa", max_length=256, required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'cedula', 'rolUsuario', 'password1', 'password2', 'foto_perfil', 'foto_auth', 'urlFramework', 'frameworkToken', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            raise forms.ValidationError('Este email ya esta en uso. Porfavor introduzca otro email')
        return email

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if cedula and Usuario.objects.filter(cedula=cedula).exclude(cedula=cedula).count():
            raise forms.ValidationError('Esta Cedula ya esta en uso por favor introducir otra cedula')
        # if re.match(cedula_regex,cedula) is None:
        #     raise forms.ValidationError('La cedula debe estar en formato V000000000')
        return cedula


class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(label='Nombre', max_length='30')
    last_name = forms.CharField(label='Apellido', max_length='30')
    cedula = forms.CharField(label='Cedula', max_length='10')
    email = forms.EmailField(label='Correo Electronico', max_length='254')
    rolChoices = (
        (3, 'Usuario Comun'),
        (1, 'Administrador de Sistema'),
        (2, 'Administrador de Framework'),
        )
    rolUsuario = forms.MultipleChoiceField(label='Rol del Usuario en el Sistema', choices=rolChoices,  widget=forms.CheckboxSelectMultiple, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(username=email).count():
            raise forms.ValidationError('Este email ya esta en uso. Porfavor introduzca otro email')
        return email

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if cedula and Usuario.objects.filter(cedula=cedula).exclude(cedula=cedula).count():
            raise forms.ValidationError('Esta Cedula ya esta en uso por favor introducir otra cedula')
        return cedula


class UpdateUserForm(forms.Form):
    first_name = forms.CharField(label='Nombre', max_length='30')
    last_name = forms.CharField(label='Apellido', max_length='30')
    cedula = forms.CharField(label='Cedula', max_length='10')
    email = forms.EmailField(label='Correo Electronico', max_length='254')
    rolChoices = (
        (3, 'Usuario Comun'),
        (1, 'Administrador de Sistema'),
        (2, 'Administrador de Framework'),
        )
    rolUsuario = forms.MultipleChoiceField(label='Rol del Usuario en el Sistema', choices=rolChoices, widget=forms.CheckboxSelectMultiple)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(username=email).count():
            raise forms.ValidationError('Este email ya esta en uso. Porfavor introduzca otro email')
        return email

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if cedula and Usuario.objects.filter(cedula=cedula).exclude(cedula=cedula).count():
            raise forms.ValidationError('Esta Cedula ya esta en uso por favor introducir otra cedula')
        return cedula


class FrameworkUpdateForm(forms.Form):
    urlFramework = forms.CharField(label='URL del Framework', max_length='50')
    frameworkToken = forms.CharField(label='Token del API externa', max_length='256')

    def clean_urlFramework(self):
        urlFramework = self.cleaned_data.get('urlFramework')
        if urlFramework and Framework.objects.filter(urlFramework=urlFramework).exclude(urlFramework=urlFramework).count():
            raise forms.ValidationError('Esta URL ya esta en uso, por favor introduzca una url valida')
        return urlFramework


class FrameworkCreateForm(forms.Form):
    urlFramework = forms.CharField(label='URL del Framework', max_length='50')
    frameworkToken = forms.CharField(label='Token del API externa', max_length='256')

    def clean_urlFramework(self):
        urlFramework = self.cleaned_data.get('urlFramework')
        if urlFramework and Framework.objects.filter(urlFramework=urlFramework).count():
            raise forms.ValidationError('Esta URL ya esta en uso, por favor introduzca una url valida')
        return urlFramework


class CustomLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if user.is_active is False:
            raise forms.ValidationError(_('Esta cuenta esta inactiva, reportarse con el administrador del sistema'),
                code='inactiva')
