from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Direccion

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario o correo electrónico', widget=forms.TextInput(attrs={
        'placeholder': 'Nombre de Usuario o Correo Electrónico',
        'class': 'w-full px-4 py-2 border rounded-xl'
    }))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={
        'placeholder': 'Contraseña',
        'class': 'w-full px-4 py-2 border rounded-xl'
    }))

# Definimos el formulario de registro
class SignupForm(UserCreationForm):
    # Definimos los campos del formulario
    # Nota: los atributos 'attrs' definen los atributos HTML de los campos del formulario
    # 'required' define si el campo es obligatorio o no
    # 'max_length' define la longitud máxima del campo
    # Los diferentes tipos de campos (CharField, EmailField, BooleanField, etc.) representan diferentes tipos de datos
    username = forms.CharField(label = 'Usuario', widget=forms.TextInput(attrs={
        'placeholder': 'Nombre de usuario',
        'class': 'w-full px-4 py-2 border rounded-xl'
    }))
    first_name = forms.CharField(label = 'Nombre', widget=forms.TextInput(attrs={
        'placeholder': 'Nombre',
        'class': 'w-full px-4 py-2 border rounded-xl'
    }), required=True)
    last_name = forms.CharField(label = 'Apellidos', widget=forms.TextInput(attrs={
        'placeholder': 'Apellido',
        'class': 'w-full px-4 py-2 border rounded-xl'
    }), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Correo electrónico',
        'class': 'w-full px-4 py-2 border rounded-xl'
    }))
    password1 = forms.CharField(label = 'Contraseña', widget=forms.PasswordInput(attrs={
        'placeholder': 'Contraseña',
        'class': 'w-full px-4 py-2 border rounded-xl'
    }))
    password2 = forms.CharField(label = 'Repetir Contraseña', widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmación de contraseña',
        'class': 'w-full px-4 py-2 border rounded-xl'
    }))
    vendedor = forms.BooleanField(label='Vendedor', required=False, widget=forms.CheckboxInput(attrs={
        'class': 'leading-tight'
    }))
    biografia = forms.CharField(label='Biografía', required=False, widget=forms.Textarea(attrs={
        'placeholder': 'Biografía',
        'class': 'w-full px-4 py-2 border rounded-xl',
        'rows': 3
    }))
    cedula = forms.CharField(label='Cédula', max_length=9, widget=forms.TextInput(attrs={
        'placeholder': 'Cédula',
        'class': 'w-full px-4 py-2 border rounded-xl'
    }))
    telefono = forms.CharField(label='Teléfono', max_length=15, widget=forms.TextInput(attrs={
        'placeholder': 'Teléfono',
        'class': 'w-full px-4 py-2 border rounded-xl'
    }))
    direccion = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Dirección',
        'class': 'w-full px-4 py-2 border rounded-xl'
    }))
    ciudad = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ciudad',
        'class': 'w-full px-4 py-2 border rounded-xl'
    }))
    pais = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'País',
        'class': 'w-full px-4 py-2 border rounded-xl'
    }))
    codigo_postal = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Código Postal',
        'class': 'w-full px-4 py-2 border rounded-xl'
    }))
    
     # Aquí definimos los metadatos del formulario
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2',
                  'vendedor', 'biografia', 'cedula', 'telefono', 'direccion', 'ciudad', 'pais', 'codigo_postal']

    # Redefinimos el método save para guardar los datos del formulario en el modelo
    def save(self, commit=True):
        user = super().save(commit=False)  # Creamos un nuevo usuario pero no lo guardamos en la base de datos todavía
        # Asignamos los datos del formulario al usuario
        user.vendedor = self.cleaned_data.get('vendedor')
        user.biografia = self.cleaned_data.get('biografia')
        user.cedula = self.cleaned_data.get('cedula')
        user.telefono = self.cleaned_data.get('telefono')
        if commit:  # Si commit es True, guardamos el usuario en la base de datos
            user.save()
            # Creamos una nueva dirección para el usuario con los datos del formulario
            Direccion.objects.create(
                usuario=user,
                direccion=self.cleaned_data.get('direccion'),
                ciudad=self.cleaned_data.get('ciudad'),
                pais=self.cleaned_data.get('pais'),
                codigo_postal=self.cleaned_data.get('codigo_postal')
            )
        return user  # Devolvemos el usuario creado