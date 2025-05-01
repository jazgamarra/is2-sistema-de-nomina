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
class Empleado(models.Model):
    id_empleado = id_empleado = models.AutoField(primary_key=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento', blank=True, null=True)
    #id_cargo = models.ForeignKey(Cargo, models.DO_NOTHING, db_column='id_cargo', blank=True, null=True)
    nombres = models.CharField()
    apellidos = models.CharField()
    cedula = models.IntegerField()
    fecha_nacimiento = models.DateField()
    telefono = models.IntegerField()
    email = models.CharField()
    fecha_ingreso = models.DateField()
    activo = models.BooleanField()

    hijos_menores_18 = models.IntegerField(default=0)
    aplica_ips = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"  # Esto mostrará el nombre completo del empleado


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