from django.db import models
from empleado.models import Empleado

class Liquidacion(models.Model):
    id_liquidacion = models.IntegerField(primary_key=True)
    fecha_liquidacion = models.DateField()
    fecha_pago = models.DateField()
    mes_liquidacion = models.IntegerField()
    anho_liquidacion = models.IntegerField()
    id_empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='id_empleado', blank=True, null=True)

    class Meta:
        
        db_table = 'liquidacion'

class Concepto(models.Model):
    id_concepto = models.IntegerField(primary_key=True)
    descripcion = models.CharField()
    es_fijo = models.BooleanField()
    es_deb_cred = models.BooleanField()
    porcentaje = models.DecimalField(max_digits=5, decimal_places=5)
    permite_cuotas = models.BooleanField()
    cant_cuotas = models.IntegerField()

    class Meta:
        
        db_table = 'concepto'

class ConceptoLiquidacion(models.Model):
    id_liquidacion = models.ForeignKey('Liquidacion', models.DO_NOTHING, db_column='id_liquidacion', blank=True, null=True)
    id_concepto = models.ForeignKey(Concepto, models.DO_NOTHING, db_column='id_concepto', blank=True, null=True)
    monto_concepto = models.DecimalField(max_digits=20, decimal_places=5)

    class Meta:
        
        db_table = 'concepto_liquidacion'

class DebCredMes(models.Model):
    id = models.IntegerField(primary_key=True)
    id_empleado = models.IntegerField(blank=True, null=True)
    id_concepto = models.ForeignKey(Concepto, models.DO_NOTHING, db_column='id_concepto', blank=True, null=True)
    mes = models.IntegerField()
    anho = models.IntegerField()
    monto = models.DecimalField(max_digits=15, decimal_places=5)

    class Meta:
        
        db_table = 'deb_cred_mes'

