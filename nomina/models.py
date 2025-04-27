from django.db import models

class Cargo(models.Model):
    id_cargo = models.IntegerField(primary_key=True)
    nombre_cargo = models.CharField()

    class Meta:
        db_table = 'cargo'

    def __str__(self):
        return self.nombre_cargo 


class Departamento(models.Model):
    id_departamento = models.IntegerField(primary_key=True)
    departamento = models.CharField()

    def __str__(self):
        return self.departamento 

    class Meta:
        db_table = 'departamento'


# class Contrato(models.Model):
#     id_contrato = models.IntegerField(primary_key=True)
#     id_empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='id_empleado', blank=True, null=True)
#     tipo_contrato = models.CharField()
#     fecha_inicio = models.DateField()
#     fecha_fin = models.DateField()
#     tiene_beneficios = models.BooleanField()
#     salario_acordado = models.DecimalField(max_digits=15, decimal_places=5)
#     contrato_activo = models.BooleanField()

#     def __str__(self):
#         salario = f"{int(self.salario_acordado)}" if self.salario_acordado else "No definido"
#         return f"{self.id_contrato} | {self.tipo_contrato} | {self.fecha_inicio} | {salario}" 
    
#     class Meta:
#         db_table = 'contrato'
        
# class HistorialEmpleado(models.Model):
#     id_auditoria = models.IntegerField(primary_key=True)
#     id_empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='id_empleado', blank=True, null=True)
#     accion = models.CharField()
#     campo_afectado = models.CharField()
#     valor_anterior = models.CharField()
#     valor_nuevo = models.CharField()
#     fecha_accion = models.DateField()
#     usuario_que_realizo = models.CharField()

#     class Meta:
        
#         db_table = 'historial_empleado'




# class SaldoDescuento(models.Model):
#     id_saldo_descuento = models.IntegerField(primary_key=True)
#     id_empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='id_empleado', blank=True, null=True)
#     id_concepto = models.ForeignKey(Concepto, models.DO_NOTHING, db_column='id_concepto', blank=True, null=True)
#     monto_total = models.DecimalField(max_digits=15, decimal_places=5)
#     monto_pendiente = models.DecimalField(max_digits=15, decimal_places=5)
#     monto_cuota = models.DecimalField(max_digits=15, decimal_places=5)
#     fecha_inicio = models.DateField()
#     fecha_fin = models.DateField()
#     estado = models.BooleanField()

#     class Meta:
        
#         db_table = 'saldo_descuento'
