from django.db import models

class Concepto(models.Model):
    descripcion = models.CharField(max_length=255)
    es_fijo = models.BooleanField(default=False)
    es_deb_cred = models.BooleanField(default=False)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    permite_cuotas = models.BooleanField(default=False)
    cant_cuota = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.descripcion
