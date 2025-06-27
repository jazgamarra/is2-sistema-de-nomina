from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_list_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django import forms


def login_view(request):
    if request.user.is_authenticated:
        return redirect('listar_empleados')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('listar_empleados')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_staff', 'is_active']

@login_required
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})

@login_required
def crear_usuario(request):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        if form.cleaned_data['password']:
            user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(request, "Usuario creado correctamente.")
        return redirect('listar_usuarios')
    return render(request, 'usuarios/form_usuario.html', {'form': form})

@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    form = UsuarioForm(request.POST or None, instance=usuario)
    if form.is_valid():
        user = form.save(commit=False)
        if form.cleaned_data['password']:
            user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect('listar_usuarios')
    return render(request, 'usuarios/form_usuario.html', {'form': form})

@login_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    usuario.delete()
    messages.success(request, "Usuario eliminado.")
    return redirect('listar_usuarios')
