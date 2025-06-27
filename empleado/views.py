from django.shortcuts import render, redirect, get_object_or_404
from empleado.models import Empleado, Departamento
from empleado.forms import EmpleadoForm, DepartamentoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Vista para listar empleados
@login_required
def listar_empleados(request):
    empleados = Empleado.objects.all().order_by('-activo', 'apellidos', 'nombres')
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

def eliminar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.activo = False
        empleado.save()
        return redirect('listar_empleados')
    return render(request, 'empleado/eliminar_empleado.html', {'empleado': empleado})

def listar_departamentos(request):
    departamentos = Departamento.objects.all()
    return render(request, 'departamento/listar.html', {'departamentos': departamentos})

def crear_departamento(request):
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento creado exitosamente.')
            return redirect('listar_departamentos')
    else:
        form = DepartamentoForm()
    return render(request, 'departamento/formulario.html', {'form': form})

def editar_departamento(request, pk):
    departamento = get_object_or_404(Departamento, pk=pk)
    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento actualizado.')
            return redirect('listar_departamentos')
    else:
        form = DepartamentoForm(instance=departamento)
    return render(request, 'departamento/formulario.html', {'form': form})

def eliminar_departamento(request, pk):
    departamento = get_object_or_404(Departamento, pk=pk)
    if request.method == 'POST':
        departamento.delete()
        messages.success(request, 'Departamento eliminado.')
        return redirect('listar_departamentos')
    return render(request, 'departamento/confirmar_eliminar.html', {'departamento': departamento})
