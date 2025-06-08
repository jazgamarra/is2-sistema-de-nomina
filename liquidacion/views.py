from django.shortcuts import render, get_object_or_404,redirect
from empleado.models import Empleado
from liquidacion.models import Concepto, ConceptoLiquidacion
from liquidacion.forms import ConceptoForm
from django.contrib.auth.decorators import login_required
from .services import calcular_sueldo_detallado
import json


# Vista para listar empleados
def listar_empleados_reporte(request):
    empleados = Empleado.objects.all()
    return render(request, 'liquidacion/lista_empleados.html', {'empleados': empleados})

# Vista para ver nómina de un empleado
# dentro de views.py
def ver_nomina_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id_empleado=empleado_id)

    # Obtener sueldo detallado
    sueldo_detallado = calcular_sueldo_detallado(empleado_id)

    salario_base = sueldo_detallado['salario_base']
    bonificacion_total = sueldo_detallado['bonificaciones']
    descuento_total = sueldo_detallado['descuentos']
    sueldo_total = sueldo_detallado['sueldo_total']

    context = {
        'empleado': empleado,
        'salario_base': salario_base,
        'bonificacion_total': bonificacion_total,  
        'descuento_total': descuento_total,        
        'sueldo_total': sueldo_total,
    }
    return render(request, 'liquidacion/reporte_nomina.html', context)

# VIEWS DE CONCEPTO
#Agregué la parte de concepto ya que está está declarada en el models de ésta app
@login_required
def listar_conceptos(request):
    conceptos = Concepto.objects.all()
    return render(request, 'concepto/listar_concepto.html', {'conceptos': conceptos})

@login_required
def crear_concepto(request):
    if request.method == 'POST':
        form = ConceptoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_conceptos')
        else:
            print(form.errors)  # Ver errores en la consola del servidor
    else:
        form = ConceptoForm()
    return render(request, 'concepto/crear_concepto.html', {'form': form})

@login_required
def editar_concepto(request, pk):
    concepto = get_object_or_404(Concepto, pk=pk)
    if request.method == 'POST':
        form = ConceptoForm(request.POST, instance=concepto)
        if form.is_valid():
            form.save()
            return redirect('listar_conceptos')
    else:
        form = ConceptoForm(instance=concepto)
    return render(request, 'concepto/editar_concepto.html', {'form': form})

@login_required
def eliminar_concepto(request, pk):
    concepto = get_object_or_404(Concepto, pk=pk)
    if request.method == 'POST':
        concepto.delete()  # Elimina físicamente el concepto
        return redirect('listar_conceptos')
    return render(request, 'concepto/eliminar_concepto.html', {'concepto': concepto})

# Vistas para cargar concepto por empleado 
def cargar_conceptos_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, pk=empleado_id)
    conceptos = Concepto.objects.all()
    return render(request, 'liquidacion/cargar_conceptos.html', {
        'empleado': empleado,
        'conceptos': conceptos
    })

def guardar_conceptos(request, empleado_id):
    if request.method == 'POST':
        conceptos_data = json.loads(request.POST.get('conceptos_json', '[]'))
        for item in conceptos_data:
            concepto = Concepto.objects.get(pk=item['id_concepto'])
            monto = item['monto']
            ConceptoLiquidacion.objects.create(
                id_concepto=concepto,
                id_liquidacion=None,  
                monto_concepto=monto
            )
        return redirect('listar_empleados') 

# Vistas para gestionar nominas 
def gestionar_nominas(request):
    return render(request, 'liquidacion/gestionar_nominas.html')

def generar_nomina(request):
    return render(request, 'liquidacion/generar_nomina.html')

def listar_empleados_para_concepto(request):
    empleados = Empleado.objects.all()
    return render(request, 'liquidacion/lista_empleados_concepto.html', {
        'empleados': empleados
    })