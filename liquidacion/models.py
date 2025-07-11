from django.db import models
from empleado.models import Empleado

class Liquidacion(models.Model):
    id_liquidacion = models.AutoField(primary_key=True)
    fecha_liquidacion = models.DateField()
    fecha_pago = models.DateField()
    mes_liquidacion = models.IntegerField()
    anho_liquidacion = models.IntegerField()

    class Meta: 
        
        db_table = 'liquidacion'

class Concepto(models.Model):
    id_concepto = models.AutoField(primary_key=True)
    descripcion = models.CharField()
    es_fijo = models.BooleanField()
    es_deb_cred = models.BooleanField()
    porcentaje = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    permite_cuotas = models.BooleanField(null=True)
    cant_cuotas = models.IntegerField(null=True)

    class Meta:
        
          db_table = 'concepto'
    
    def __str__(self):
        return self.descripcion 

class ConceptoLiquidacion(models.Model):
    id_concepto_liquidacion = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='id_empleado', blank=True, null=True)
    id_concepto = models.ForeignKey(Concepto, models.DO_NOTHING, db_column='id_concepto', blank=True, null=True)
    monto = models.DecimalField(max_digits=20, decimal_places=5)

    class Meta:

        db_table = 'concepto_liquidacion'

class ConcEmpLiquidacion(models.Model):
    id_liquidacion = models.ForeignKey(Liquidacion, models.DO_NOTHING, db_column='id_liquidacion', blank=True, null=True)
    id_concepto_liquidacion = models.ForeignKey(ConceptoLiquidacion, models.DO_NOTHING, db_column='id_concepto_liquidacion', blank=True, null=True)

    class Meta:
        
        db_table = 'conc_emp_liquidacion'

class DebCredMes(models.Model):
    id = models.AutoField(primary_key=True)

    id_empleado = models.ForeignKey('empleado.Empleado', on_delete=models.CASCADE, db_column="id_empleado")
    id_concepto = models.ForeignKey('Concepto', on_delete=models.CASCADE, db_column='id_concepto')
    mes = models.IntegerField()
    anho = models.IntegerField()
    monto = models.DecimalField(max_digits=15, decimal_places=5)

    class Meta:
        
        db_table = 'deb_cred_mes'
        unique_together = ('id_empleado','id_concepto','mes','anho') 

