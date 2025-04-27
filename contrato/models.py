from django.db import models
from empleado.models import Empleado

class Contrato(models.Model):
    id_contrato = models.IntegerField(primary_key=True)
    id_empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='id_empleado', blank=True, null=True)
    tipo_contrato = models.CharField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tiene_beneficios = models.BooleanField()
    salario_acordado = models.DecimalField(max_digits=15, decimal_places=5)
    contrato_activo = models.BooleanField()

    def __str__(self):
        salario = f"{int(self.salario_acordado)}" if self.salario_acordado else "No definido"
        return f"{self.id_contrato} | {self.tipo_contrato} | {self.fecha_inicio} | {salario}" 
    
    class Meta:
        db_table = 'contrato'