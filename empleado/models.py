from django.db import models
from nomina.models import Cargo, Departamento

class Empleado(models.Model):
    id_empleado = id_empleado = models.AutoField(primary_key=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento', blank=True, null=True)
    id_cargo = models.ForeignKey(Cargo, models.DO_NOTHING, db_column='id_cargo', blank=True, null=True)
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