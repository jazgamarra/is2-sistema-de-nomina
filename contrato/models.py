from django.db import models

class Contrato(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(
        "empleado.Empleado",
        on_delete=models.CASCADE,
        related_name='contratos'
    )

    
    tipo_contrato = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    salario_acordado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    contrato_activo = models.BooleanField(default=True)
    tiene_beneficios = models.BooleanField(default=False)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contrato'
        ordering = ['-contrato_activo', 'fecha_inicio']

    def __str__(self):
        return f"Contrato {self.id_contrato} - {self.tipo_contrato} ({self.id_empleado.nombres} {self.id_empleado.apellidos})"
