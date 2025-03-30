# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Cargo(models.Model):
    id_cargo = models.IntegerField(primary_key=True)
    nombre_cargo = models.CharField()

    class Meta:
        
        db_table = 'cargo'


class Concepto(models.Model):
    id_concepto = models.IntegerField(primary_key=True)
    descripcion = models.CharField()
    es_fijo = models.BooleanField()
    es_deb_cred = models.BooleanField()
    porcentaje = models.DecimalField(max_digits=65535, decimal_places=65535)
    permite_cuotas = models.BooleanField()
    cant_cuotas = models.IntegerField()

    class Meta:
        
        db_table = 'concepto'


class ConceptoLiquidacion(models.Model):
    id_liquidacion = models.ForeignKey('Liquidacion', models.DO_NOTHING, db_column='id_liquidacion', blank=True, null=True)
    id_concepto = models.ForeignKey(Concepto, models.DO_NOTHING, db_column='id_concepto', blank=True, null=True)
    id_empleado = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='id_empleado', blank=True, null=True)
    monto_concepto = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        
        db_table = 'concepto_liquidacion'


class Contrato(models.Model):
    id_contrato = models.IntegerField(primary_key=True)
    id_cargo = models.ForeignKey(Cargo, models.DO_NOTHING, db_column='id_cargo', blank=True, null=True)
    tipo_contrato = models.CharField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tiene_beneficios = models.BooleanField()
    salario_acordado = models.DecimalField(max_digits=65535, decimal_places=65535)
    contrato_activo = models.BooleanField()

    class Meta:
        
        db_table = 'contrato'


class DebCredMes(models.Model):
    id = models.IntegerField(primary_key=True)
    id_empleado = models.IntegerField(blank=True, null=True)
    id_concepto = models.ForeignKey(Concepto, models.DO_NOTHING, db_column='id_concepto', blank=True, null=True)
    mes = models.IntegerField()
    anho = models.IntegerField()
    monto = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        
        db_table = 'deb_cred_mes'


class Departamento(models.Model):
    id_departamento = models.IntegerField(primary_key=True)
    departamento = models.CharField()

    class Meta:
        
        db_table = 'departamento'


class Empleado(models.Model):
    id_empleado = models.IntegerField(primary_key=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento', blank=True, null=True)
    id_contrato = models.ForeignKey(Contrato, models.DO_NOTHING, db_column='id_contrato', blank=True, null=True)
    nombres = models.CharField()
    apellidos = models.CharField()
    cedula = models.IntegerField()
    fecha_nacimiento = models.DateField()
    telefono = models.IntegerField()
    email = models.CharField()
    fecha_ingreso = models.DateField()
    activo = models.BooleanField()

    class Meta:
        
        db_table = 'empleado'


class HistorialEmpleado(models.Model):
    id_auditoria = models.IntegerField(primary_key=True)
    id_empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='id_empleado', blank=True, null=True)
    accion = models.CharField()
    campo_afectado = models.CharField()
    valor_anterior = models.CharField()
    valor_nuevo = models.CharField()
    fecha_accion = models.DateField()
    usuario_que_realizo = models.CharField()

    class Meta:
        
        db_table = 'historial_empleado'


class Liquidacion(models.Model):
    id_liquidacion = models.IntegerField(primary_key=True)
    fecha_liquidacion = models.DateField()
    fecha_pago = models.DateField()
    mes_liquidacion = models.IntegerField()
    anho_liquidacion = models.IntegerField()

    class Meta:
        
        db_table = 'liquidacion'


class SaldoDescuento(models.Model):
    id_saldo_descuento = models.IntegerField(primary_key=True)
    id_empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='id_empleado', blank=True, null=True)
    id_concepto = models.ForeignKey(Concepto, models.DO_NOTHING, db_column='id_concepto', blank=True, null=True)
    monto_total = models.DecimalField(max_digits=65535, decimal_places=65535)
    monto_pendiente = models.DecimalField(max_digits=65535, decimal_places=65535)
    monto_cuota = models.DecimalField(max_digits=65535, decimal_places=65535)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.BooleanField()

    class Meta:
        
        db_table = 'saldo_descuento'
