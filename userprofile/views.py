# Importamos los módulos necesarios de Django
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Direccion
from .forms import LoginForm, SignupForm, UsuarioForm, DireccionForm  # Importamos los formularios que hemos definido

# Definimos la vista para el registro de usuarios
def signup_view(request):
    # Si el usuario ya está autenticado, lo redirigimos a la página de inicio
    if request.user.is_authenticated:
        return redirect('core:home')  
    # Si el método de la petición es POST, procesamos el formulario
    if request.method == 'POST':
        form = SignupForm(request.POST)  # Creamos un formulario con los datos de la petición
        # Si el formulario es válido, lo guardamos y redirigimos al usuario a la página de inicio de sesión
        if form.is_valid():
            form.save()
            return redirect('userprofile:login')
    # Si el método de la petición no es POST, mostramos el formulario vacío
    else:
        form = SignupForm()
    # Renderizamos la plantilla de registro con el formulario
    return render(request, 'userprofile/signup.html', {'form': form})

# Definimos la vista para el inicio de sesión de usuarios
def login_view(request):
    # Si el usuario ya está autenticado, lo redirigimos a la página de inicio
    if request.user.is_authenticated:
        return redirect('core:home')  
    # Si el método de la petición es POST, procesamos el formulario
    if request.method == 'POST':
        form = LoginForm(data=request.POST)  # Creamos un formulario con los datos de la petición
        # Si el formulario es válido, autenticamos al usuario
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            # Si el usuario es autenticado con éxito, iniciamos su sesión y lo redirigimos a la página de inicio
            if user is not None:
                login(request, user)
                return redirect('core:home')
    # Si el método de la petición no es POST, mostramos el formulario vacío
    else:
        form = LoginForm()
    # Renderizamos la plantilla de inicio de sesión con el formulario
    return render(request, 'userprofile/login.html', {'form': form})

@login_required
def perfil(request):
    if request.method == 'POST':
        user_form = UsuarioForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('userprofile:perfil')
    else:
        user_form = UsuarioForm(instance=request.user)

    direcciones = Direccion.objects.filter(usuario=request.user)
    direccion_form = DireccionForm()
    return render(request, 'userprofile/perfil.html', {
        'user_form': user_form,
        'direccion_form': direccion_form,
        'direcciones': direcciones
    })
    
@login_required    
def agregar_direccion(request):
    if request.method == 'POST':
        direccion_form = DireccionForm(request.POST)
        if direccion_form.is_valid():
            direccion = direccion_form.save(commit=False)
            direccion.usuario = request.user
            direccion.save()
            return redirect('userprofile:perfil')
    return redirect('userprofile:perfil')

@login_required    
def editar_direccion(request, id):
    direccion = get_object_or_404(Direccion, id=id, usuario=request.user)
    if request.method == 'POST':
        direccion_form = DireccionForm(request.POST, instance=direccion)
        if direccion_form.is_valid():
            direccion_form.save()
            return redirect('userprofile:perfil')
    else:
        direccion_form = DireccionForm(instance=direccion)
    return render(request, 'userprofile/editar_direccion.html', {
        'direccion_form': direccion_form,
        'direccion': direccion
    })


@login_required    
def eliminar_direccion(request, id):
    direccion = Direccion.objects.get(id=id)
    direccion.delete()
    return redirect('userprofile:perfil')
