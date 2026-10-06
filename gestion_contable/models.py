from django.core.exceptions import ValidationError
from django.db import models
from gestion_escrituracion.models import Venta
from utils_project.choices import PAGOS_CHOICES


# Create your models here.

class Bancos(models.Model):
    id_banco = models.AutoField(primary_key=True)
    nombre_banco = models.CharField(verbose_name="Nombre Banco", max_length=50)

    class Meta:
        db_table = 'banco'
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        #unique_together = (('partida', 'id'),)
        ordering = ['nombre_banco']
    def __str__(self):
        return str(self.id_banco)+ " - " +str(self.nombre_banco)


class CategoriaPago(models.Model):
    id_categoria_pago = models.AutoField(primary_key=True)
    nombre_categoria_pago = models.CharField(verbose_name="Nombre Categoria", max_length=50)

    class Meta:
        db_table = 'categoria_pago'
        verbose_name = 'Categoria Pago'
        verbose_name_plural = 'Categorias Pagos'
        #unique_together = (('partida', 'id'),)
        ordering = ['id_categoria_pago']
    def __str__(self):
        return str(self.id_categoria_pago)+ " - " +str(self.nombre_categoria_pago)

class FormaPago(models.Model):
    id_forma_pago = models.AutoField(primary_key=True)
    nombre_forma_pago = models.CharField(verbose_name="Nombre Forma", max_length=50)

    class Meta:
        db_table = 'forma_pago'
        verbose_name = 'Forma Pago'
        verbose_name_plural = 'Formas Pagos'
        #unique_together = (('partida', 'id'),)
        ordering = ['id_forma_pago']
    def __str__(self):
        return str(self.id_forma_pago)+ " - " +str(self.nombre_forma_pago)



class Pagos(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_forma_pago = models.ForeignKey(FormaPago, on_delete=models.CASCADE)
    id_categoria_pago = models.ForeignKey(CategoriaPago, on_delete=models.CASCADE)
    id_banco = models.ForeignKey(Bancos, on_delete=models.CASCADE)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    estado_pago = models.CharField(verbose_name="Estado Pago",choices=PAGOS_CHOICES, max_length=50, default=PAGOS_CHOICES[0][0])
    num_documento = models.CharField(verbose_name="Numero de Documento", max_length=50)
    fecha_registro_pago = models.DateField(verbose_name="Fecha de registro")
    fecha_real_pago = models.DateField(verbose_name="Fecha contable")
    monto_pago = models.IntegerField(verbose_name="Monto de pago")
    uf_pago = models.FloatField(verbose_name="Monto en UF", blank=True, null=True)
    observacion_pago = models.CharField(verbose_name="Observaciones de pago", max_length=100)

    class Meta:
        db_table = 'pagos'
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        #unique_together = (('partida', 'id'),)
        ordering = ['id_pago']
    def __str__(self):
        return str(self.id_pago)+ " - " +str(self.id_venta)

    def save(self, *args, **kwargs):
        if self.fecha_real_pago and self.monto_pago and self.estado_pago == "Contabilizado":
            try:
                uf = ValorUf.objects.get(fecha_registro=self.fecha_real_pago)
                self.uf_pago = round(self.monto_pago / uf.valor_uf, 2)
            except ValorUf  .DoesNotExist:
                raise ValidationError(
                    f"No se encontró valor UF para la fecha contable {self.fecha_real_pago}."
                )
        else:
            self.uf_pago = None  # 👈 limpia el campo si no aplica

        super().save(*args, **kwargs)


class ValorUf(models.Model):
    id_valor_uf = models.AutoField(primary_key=True)
    fecha_registro = models.DateField(
        verbose_name="Fecha de registro",
        unique=True,
    )
    valor_uf = models.FloatField(verbose_name="Valor de UF")

    class Meta:
        db_table = 'valor_uf'
        verbose_name = 'Valor de UF'
        verbose_name_plural = 'Valores de UF'
        ordering = ['fecha_registro']

    def __str__(self):
        return str(self.fecha_registro)+ " - " +str(self.valor_uf)