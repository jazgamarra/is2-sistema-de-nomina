from django.shortcuts import render, get_object_or_404, redirect
from .models import Contrato
from .forms import ContratoForm
from django.contrib.auth.decorators import login_required
from empleado.models import Empleado  # Importa el modelo Empleado

@login_required
def listar_contratos(request):
    contratos = Contrato.objects.all().order_by('-contrato_activo', 'fecha_inicio')
    return render(request, 'Contrato/listar_contratos.html', {'contratos': contratos})

@login_required
def listar_contratos_empleado(request, empleado_id):
    contratos = Contrato.objects.filter(id_empleado=empleado_id).order_by('-contrato_activo', 'fecha_inicio')
    return render(request, 'Contrato/listar_contratos.html', {'contratos': contratos})

@login_required
def crear_contrato(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_contratos')
    else:
        form = ContratoForm()
    return render(request, 'contrato/crear_contrato.html', {'form': form})

@login_required
def crear_contrato_empleado(request, empleado_id):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.id_empleado = get_object_or_404(Empleado, pk=empleado_id)  # Relaciona el contrato con el empleado
            contrato.save()
            return redirect('listar_contratos_empleado', empleado_id=empleado_id)
    else:
        form = ContratoForm()
    return render(request, 'contrato/crear_contrato.html', {'form': form})

@login_required
def editar_contrato(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    if request.method == 'POST':
        form = ContratoForm(request.POST, instance=contrato)
        if form.is_valid():
            form.save()
            return redirect('listar_contratos')
    else:
        form = ContratoForm(instance=contrato)
    return render(request, 'Contrato/editar_contrato.html', {'form': form})

@login_required
def editar_contrato_empleado(request, empleado_id, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    if request.method == 'POST':
        form = ContratoForm(request.POST, instance=contrato)
        if form.is_valid():
            form.save()
            return redirect('listar_contratos_empleado', empleado_id=empleado_id)
    else:
        form = ContratoForm(instance=contrato)
    return render(request, 'Contrato/editar_contrato.html', {'form': form})

@login_required
def eliminar_contrato(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    if request.method == 'POST':
        contrato.contrato_activo = False
        contrato.save()
        return redirect('listar_contratos')
    return render(request, 'Contrato/eliminar_contrato.html', {'contrato': contrato})

@login_required
def eliminar_contrato_empleado(request, empleado_id, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    if request.method == 'POST':
        contrato.contrato_activo = False
        contrato.save()
        return redirect('listar_contratos_empleado', empleado_id=empleado_id)
    return render(request, 'Contrato/eliminar_contrato.html', {'contrato': contrato})
