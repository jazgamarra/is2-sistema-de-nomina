from django.shortcuts import render, get_object_or_404,redirect
from empleado.models import Empleado
from liquidacion.models import Concepto, ConceptoLiquidacion, DebCredMes, ConcEmpLiquidacion, Liquidacion
from liquidacion.forms import ConceptoForm
from django.contrib.auth.decorators import login_required
import json
from datetime import date
from django.contrib import messages
from .services import calcular_sueldo_detallado
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from .models import DebCredMes  # Importá tu modelo corregido
from django.db import transaction
from num2words import num2words
from .models import DebCredMes  # asegurate de tener el import
from django.contrib.messages import get_messages
from decimal import Decimal

from django.utils.timezone import now

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
    list(get_messages(request))  # Limpia los mensajes previos

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


# Vistas para gestionar nominas 
def gestionar_nominas(request):
    return render(request, 'liquidacion/gestionar_nominas.html')

def listar_empleados_para_concepto(request):
    empleados = Empleado.objects.all()
    return render(request, 'liquidacion/listar_empleados_para_concepto.html', {
        'empleados': empleados
    })

@login_required
def generar_nomina(request):
    empleados = Empleado.objects.all()
    cedula = request.GET.get("cedula")
    if cedula:
        empleados = empleados.filter(cedula=cedula)

    nominas = []
    mes = request.GET.get("mes") or request.POST.get("mes")
    anho = request.GET.get("anho") or request.POST.get("anho")

    if mes and anho:
        mes = int(mes)
        anho = int(anho)
        for emp in empleados:
            datos = calcular_sueldo_detallado(emp.id_empleado, mes=mes, anho=anho)
            nominas.append({    
                'empleado': emp,
                'salario': datos['salario_base'],
                'bonos': datos['bonificaciones'],
                'descuentos': datos['descuentos'],
                'total': datos['sueldo_total'],
            })

    # Si el usuario envió POST para guardar nómina
    if request.method == "POST" and mes and anho:
        for emp in empleados:
            datos = calcular_sueldo_detallado(emp.id_empleado, mes=mes, anho=anho)

            liquidacion = Liquidacion.objects.create(
                fecha_liquidacion=date.today(),
                fecha_pago=date.today(),
                mes_liquidacion=mes,
                anho_liquidacion=anho
            )

            concepto_base = ConceptoLiquidacion.objects.create(
                id_empleado=emp,
                id_concepto=None,
                monto=datos['salario_base']
            )
            ConcEmpLiquidacion.objects.create(
                id_liquidacion=liquidacion,
                id_concepto_liquidacion=concepto_base
            )

            conceptos_asociados = DebCredMes.objects.filter(
            id_empleado=emp,
            mes=mes,
            anho=anho
            )

        for concepto in conceptos_asociados:
            cl = ConceptoLiquidacion.objects.create(
                id_empleado=emp,
                id_concepto=concepto.id_concepto,
                monto=concepto.monto
            )
            ConcEmpLiquidacion.objects.create(
                id_liquidacion=liquidacion,
                id_concepto_liquidacion=cl
            )

    messages.success(request, f"Nómina generada correctamente para {mes}/{anho}.")

    return render(request, "liquidacion/generar_nomina.html", {
        'nominas': nominas,
        'cedula': cedula or '',
        'mes': mes,
        'anho': anho
    })

# Cargar conceptos por empleado 
@login_required
def editar_conceptos_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, pk=empleado_id)
    conceptos = Concepto.objects.all()

    if request.method == 'POST':
        try:
            data = json.loads(request.POST.get('conceptos_json', '[]'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos inválidos'}, status=400)

        if not data:
            messages.warning(request, "No se cargaron conceptos.")
            return redirect(request.path)

        with transaction.atomic():
            for item in data:
                id_concepto = item.get('id_concepto')
                monto = item.get('monto')
                mes = item.get('mes')
                anho = item.get('anho')

                if not all([id_concepto, monto, mes, anho]):
                    continue  # saltea registros incompletos

                concepto = get_object_or_404(Concepto, pk=id_concepto)

                DebCredMes.objects.update_or_create(
                    id_empleado=empleado,
                    id_concepto=concepto,
                    mes=mes,
                    anho=anho,
                    defaults={'monto': monto}
                )

            messages.success(request, "Conceptos guardados correctamente.")
            return redirect(request.path)

    # GET - carga actual de conceptos desde DebCredMes
    conceptos_actuales_qs = DebCredMes.objects.filter(id_empleado=empleado)
    conceptos_actuales = []

    for cl in conceptos_actuales_qs:
        concepto = cl.id_concepto
        if concepto is None:
            continue
        registro = {
            "id_concepto": concepto.id_concepto,
            "monto": float(cl.monto),
            "mes": cl.mes,
            "anho": cl.anho,
        }
        conceptos_actuales.append(registro)

    return render(request, 'liquidacion/editar_conceptos.html', {
        'empleado': empleado,
        'conceptos': conceptos,
        'conceptos_actuales_json': json.dumps(conceptos_actuales, cls=DjangoJSONEncoder)
    })

from django.http import HttpResponse
import pdfkit
from django.template.loader import render_to_string

@login_required
def generar_pdf_recibo(request, empleado_id, liquidacion_id):
    empleado = get_object_or_404(Empleado, pk=empleado_id)
    liquidacion = get_object_or_404(Liquidacion, pk=liquidacion_id)

    conceptos = ConcEmpLiquidacion.objects.filter(
        id_liquidacion=liquidacion
    ).select_related('id_concepto_liquidacion')

    ingresos, descuentos = [], []
    total_ingresos = total_descuentos = Decimal('0')
    sueldo_base_val = Decimal('0')

    for item in conceptos:
        concepto_liq = item.id_concepto_liquidacion
        concepto = concepto_liq.id_concepto if concepto_liq else None
        monto = concepto_liq.monto if concepto_liq else 0

        if concepto is None:
            # Caso especial: sueldo base sin concepto
            sueldo_base_val += monto
            continue

        descripcion = concepto.descripcion.lower()

        if (
            not concepto.es_deb_cred
            or "ausencia" in descripcion
            or "tardía" in descripcion
            or "descuento" in descripcion
        ):
            descuentos.append((concepto.descripcion, abs(monto)))
            total_descuentos += abs(monto)
        else:
            ingresos.append((concepto.descripcion, monto))
            total_ingresos += monto

    neto = sueldo_base_val + total_ingresos - total_descuentos
    neto_letras = num2words(neto, lang='es').capitalize() + ' guaraníes'

    html = render_to_string('liquidacion/recibo_pdf.html', {
        'empleado': empleado,
        'liquidacion': liquidacion,
        'sueldo_base': sueldo_base_val,
        'ingresos': ingresos,
        'descuentos': descuentos,
        'neto': neto,
        'neto_letras': neto_letras,
    })
    
    config = pdfkit.configuration(wkhtmltopdf=r"C:\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdf = pdfkit.from_string(html, False, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="recibo_pago.pdf"'
    return response

from django.http import HttpResponse
import pdfkit
from django.template.loader import render_to_string

@login_required
def descargar_recibo_pdf(request, empleado_id, liquidacion_id):
    empleado = get_object_or_404(Empleado, pk=empleado_id)
    liquidacion = get_object_or_404(Liquidacion, pk=liquidacion_id)
    conceptos = ConcEmpLiquidacion.objects.filter(id_liquidacion=liquidacion).select_related('id_concepto_liquidacion')

    ingresos = []
    descuentos = []
    total_ingresos = 0
    total_descuentos = 0

    for item in conceptos:
        concepto = item.id_concepto_liquidacion.id_concepto
        monto = item.id_concepto_liquidacion.monto

        if concepto:
            if concepto.es_deb_cred:
                descuentos.append((concepto.descripcion, monto))
                total_descuentos += monto
            else:
                ingresos.append((concepto.descripcion, monto))
                total_ingresos += monto

    sueldo_base = conceptos.filter(id_concepto_liquidacion__id_concepto=None).first()
    sueldo_base_val = sueldo_base.id_concepto_liquidacion.monto if sueldo_base else 0
    neto = sueldo_base_val + total_ingresos - total_descuentos
    neto_letras = num2words(neto, lang='es').capitalize() + ' guaraníes'

    html = render_to_string('liquidacion/recibo_pdf.html', {
        'empleado': empleado,
        'liquidacion': liquidacion,
        'ingresos': ingresos,
        'descuentos': descuentos,
        'sueldo_base': sueldo_base_val,
        'neto': neto,
        'neto_letras': neto_letras,
        'usuario': request.user,
        'timestamp': now()
    })
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdf = pdfkit.from_string(html, False, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="recibo_{empleado.cedula}_{liquidacion.mes_liquidacion}_{liquidacion.anho_liquidacion}.pdf"'
    return response

@login_required
def recibo_pago(request, empleado_id):
    from datetime import datetime

    empleado = get_object_or_404(Empleado, pk=empleado_id)
    liquidaciones = Liquidacion.objects.filter(
        concempliquidacion__id_concepto_liquidacion__id_empleado=empleado
    ).distinct()

    selected_id = request.GET.get('liquidacion_id')
    try:
        selected_id_int = int(selected_id)
    except (TypeError, ValueError):
        selected_id_int = None

    if selected_id_int:
        liquidacion = get_object_or_404(Liquidacion, pk=selected_id_int)
        conceptos = ConcEmpLiquidacion.objects.filter(
            id_liquidacion=liquidacion
        ).select_related('id_concepto_liquidacion')

        ingresos = []
        descuentos = []

        for item in conceptos:
            concepto_liq = item.id_concepto_liquidacion
            concepto = concepto_liq.id_concepto if concepto_liq else None
            monto = concepto_liq.monto if concepto_liq else 0

            if concepto is None:
                    continue  # ⛔ evitar el error

            descripcion = concepto.descripcion

            if concepto.es_deb_cred:
                ingresos.append((descripcion, monto))
            else:
                descuentos.append((descripcion, abs(monto)))

        # Obtener salario_base, mes y año para cálculo exacto
        mes = liquidacion.mes_liquidacion
        anho = liquidacion.anho_liquidacion

        detalle = calcular_sueldo_detallado(empleado_id, mes, anho)

        return render(request, 'liquidacion/recibo_pago.html', {
            'empleado': empleado,
            'liquidaciones': liquidaciones,
            'conceptos': conceptos,
            'sueldo_base': detalle['salario_base'],
            'ingresos': ingresos,
            'descuentos': descuentos,
            'total_ingresos': detalle['bonificaciones'],
            'total_descuentos': detalle['descuentos'],
            'neto': detalle['sueldo_total'],
            'neto_letras': num2words(detalle['sueldo_total'], lang='es').capitalize() + ' guaraníes',
            'selected_id': selected_id_int
        })

    return render(request, 'liquidacion/recibo_pago.html', {
        'empleado': empleado,
        'liquidaciones': liquidaciones,
        'selected_id': None
    })