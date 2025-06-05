from django.shortcuts import render, get_object_or_404, redirect
from .models import Contrato
from .forms import ContratoForm
from django.contrib.auth.decorators import login_required
from empleado.models import Empleado

@login_required
def listar_contratos(request):
    contratos = Contrato.objects.select_related('id_empleado').all().order_by('-contrato_activo', 'fecha_inicio')
    return render(request, 'contrato/listar_contratos.html', {'contratos': contratos})

@login_required
def listar_contratos_empleado(request, empleado_id):
    contratos = Contrato.objects.select_related('id_empleado').filter(id_empleado=empleado_id).order_by('-contrato_activo', 'fecha_inicio')
    return render(request, 'contrato/listar_contratos.html', {'contratos': contratos})

@login_required
def crear_contrato(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_contratos')
        else:
            print(form.errors)  # Esto imprime los errores del formulario si no es válido
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
    return render(request, 'contrato/editar_contrato.html', {'form': form})

@login_required
def eliminar_contrato(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    if request.method == 'POST':
        contrato.contrato_activo = False  # ✅ Se marca como inactivo, no se elimina físicamente
        contrato.save()
        return redirect('listar_contratos')
    return render(request, 'contrato/eliminar_contrato.html', {'contrato': contrato})
