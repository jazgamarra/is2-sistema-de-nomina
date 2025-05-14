from django.db import connection
from decimal import Decimal

def calcular_sueldo_detallado(id_empleado):
    with connection.cursor() as cursor:
        # Buscar datos del empleado (hijos, aplica_ips, contrato)
        cursor.execute("""
            SELECT e.aplica_ips, e.hijos_menores_18, c.salario_acordado
            FROM empleado e
            JOIN contrato c ON c.id_empleado_id = e.id_empleado
            WHERE e.id_empleado = %s
        """, [id_empleado])
        empleado = cursor.fetchone()

        if not empleado:
            return {
                'salario_base': Decimal('0'),
                'bonificaciones': Decimal('0'),
                'descuentos': Decimal('0'),
                'sueldo_total': Decimal('0')
            }
        
        aplica_ips, hijos_menores_18, salario_base = empleado

        # Buscar todos los conceptos
        cursor.execute("""
            SELECT descripcion, es_deb_cred, porcentaje
            FROM concepto
        """)
        conceptos = cursor.fetchall()

    bonificacion_total = Decimal('0')
    descuento_total = Decimal('0')

    for descripcion, es_deb_cred, porcentaje in conceptos:
        descripcion = str(descripcion).strip().lower()
        porcentaje = Decimal(porcentaje)

        if descripcion == 'bonificacion_por_hijos' and hijos_menores_18 > 0:
            bonificacion_total += (salario_base * (porcentaje / 100)) * hijos_menores_18

        elif descripcion == 'descuento_ips' and aplica_ips:
            descuento_total += salario_base * (porcentaje / 100)

        elif descripcion == 'bono_por_productividad':
            bonificacion_total += salario_base * (porcentaje / 100)

        elif descripcion == 'premio_asistencia':
            bonificacion_total += salario_base * (porcentaje / 100)

    sueldo_total = salario_base + bonificacion_total - descuento_total

    return {
        'salario_base': salario_base,
        'bonificaciones': bonificacion_total,
        'descuentos': descuento_total,
        'sueldo_total': sueldo_total
    }
