# Create your models here.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cargo(models.Model):
    id_cargo = models.IntegerField(primary_key=True)
    nombre_cargo = models.CharField()

    class Meta:
        managed = False
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
        managed = False
        db_table = 'concepto'


class ConceptoLiquidacion(models.Model):
    id_liquidacion = models.ForeignKey('Liquidacion', models.DO_NOTHING, db_column='id_liquidacion', blank=True, null=True)
    id_concepto = models.ForeignKey(Concepto, models.DO_NOTHING, db_column='id_concepto', blank=True, null=True)
    id_empleado = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='id_empleado', blank=True, null=True)
    monto_concepto = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
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
        managed = False
        db_table = 'contrato'


class DebCredMes(models.Model):
    id = models.IntegerField(primary_key=True)
    id_empleado = models.IntegerField(blank=True, null=True)
    id_concepto = models.ForeignKey(Concepto, models.DO_NOTHING, db_column='id_concepto', blank=True, null=True)
    mes = models.IntegerField()
    anho = models.IntegerField()
    monto = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
        db_table = 'deb_cred_mes'


class Departamento(models.Model):
    id_departamento = models.IntegerField(primary_key=True)
    departamento = models.CharField()

    class Meta:
        managed = False
        db_table = 'departamento'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
        managed = False
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
        managed = False
        db_table = 'historial_empleado'


class Liquidacion(models.Model):
    id_liquidacion = models.IntegerField(primary_key=True)
    fecha_liquidacion = models.DateField()
    fecha_pago = models.DateField()
    mes_liquidacion = models.IntegerField()
    anho_liquidacion = models.IntegerField()

    class Meta:
        managed = False
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
        managed = False
        db_table = 'saldo_descuento'
