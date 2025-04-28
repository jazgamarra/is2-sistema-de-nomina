from django.db import models

class Contrato(models.Model):
    id_contrato = models.AutoField(primary_key=True)  # ID único para cada contrato
    id_empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE, related_name='contratos')  # Relación con el modelo Empleado
    tipo_contrato = models.CharField(max_length=100)  # Tipo de contrato (por ejemplo, indefinido, temporal)
    salario = models.DecimalField(max_digits=10, decimal_places=2)  # Salario asignado al contrato
    salario_acordado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Salario acordado (si es diferente al salario base)
    contrato_activo = models.BooleanField(default=True)  # Estado del contrato, si está activo o no
    tiene_beneficios = models.BooleanField(default=False)  # Si el contrato tiene beneficios adicionales
    fecha_inicio = models.DateField()  # Fecha de inicio del contrato
    fecha_fin = models.DateField(null=True, blank=True)  # Fecha de finalización del contrato (puede ser nula si es indefinido)
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha en la que se creó el contrato
    fecha_modificacion = models.DateTimeField(auto_now=True)  # Fecha de la última modificación del contrato

    # Relación con otros modelos opcionales si lo deseas
    # id_cargo = models.ForeignKey('Cargo', on_delete=models.SET_NULL, null=True, blank=True)  # Si es necesario
    # id_departamento = models.ForeignKey('Departamento', on_delete=models.SET_NULL, null=True, blank=True)  # Si es necesario

    class Meta:
        db_table = 'contrato'  # Nombre de la tabla en la base de datos
        ordering = ['-contrato_activo', 'fecha_inicio']  # Orden por contrato activo y fecha de inicio

    def __str__(self):
        return f"Contrato {self.id_contrato} - {self.tipo_contrato} ({self.id_empleado.nombres} {self.id_empleado.apellidos})" 