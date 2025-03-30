from django.shortcuts import render, redirect, get_object_or_404
from nomina.models import Empleado  # Asegúrate de que esta ruta sea correcta según tus modelos
from empleado.forms import EmpleadoForm
from django.contrib.auth.decorators import login_required

# Vista para listar empleados
@login_required
def listar_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'Empleado/listar_empleados.html', {'empleados': empleados})

# Vista para crear un nuevo empleado
@login_required
def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'Empleado/crear_empleado.html', {'form': form})

# Vista para editar un empleado
@login_required
def editar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('listar_empleados')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'Empleado/editar_empleado.html', {'form': form})

# Vista para eliminar un empleado
@login_required
def eliminar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('listar_empleados')
    return render(request, 'Empleado/eliminar_empleado.html', {'empleado': empleado})
