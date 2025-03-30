from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout

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
