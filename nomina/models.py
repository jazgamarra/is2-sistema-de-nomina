from django.db import models




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
