from django.core.exceptions import ValidationError
from django.db import models
from gestion_clientes.models import Cliente
# from gestion_contable.models import Bancos
from gestion_propiedad.models import Propiedade
from utils_project.choices import *


# Create your models here.
def validar_positivo(value):
    if value < 0:
        raise ValidationError('El valor debe ser un número positivo mayor o igual a 0.')


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True, verbose_name='ID')
    fecha_venta = models.DateField(auto_now_add=True, verbose_name="F.Venta", help_text="Fecha de Venta")
    id_propiedad = models.ForeignKey(Propiedade, on_delete=models.CASCADE,
                                     limit_choices_to={'estado_propiedad': 'Libre'})
    tipo_venta = models.CharField(
        verbose_name="Tipo",
        help_text="Tipo de venta",
        choices=TIPO_VENTA_CHOICES,
        max_length=50,
        default=TIPO_VENTA_CHOICES[0][0]
    )
    descuento_campagna = models.CharField(verbose_name="Dcto Camp", choices=SI_NO_CHOICES, max_length=2, default=no)
    uf_descuento_campagna = models.FloatField(verbose_name="Dcts Cam", help_text="Campaña dscto",
                                              validators=[validar_positivo])
    bono_pie = models.FloatField(verbose_name='Bon Pie', default=0, validators=[validar_positivo])
    aplicacion_bono = models.CharField(verbose_name="Aplicación Bono", choices=APLICACION_DSCTO_CHOICES, max_length=10,
                                       default='No Aplica')
    precio_venta = models.FloatField(verbose_name="P.Venta", help_text="Precio venta", default=0)
    credito_hipotecario = models.FloatField(verbose_name="Credito Hipotecario", validators=[validar_positivo], default=0)
    saldo_contado = models.FloatField(verbose_name="Saldo Contado", validators=[validar_positivo], null=True, blank=True)
    recursos_propio = models.FloatField(verbose_name="Recursos Propios", validators=[validar_positivo], null=True, blank=True)
    subsidio = models.FloatField(verbose_name="Subsidio", validators=[validar_positivo], null=True, blank=True)
    estado_venta = models.CharField(verbose_name='Estado', help_text="Estado Vent", choices=VENTAS_CHOICES,
                                    max_length=50, default=VENTAS_CHOICES[0][0])
    fecha_promesa = models.DateField(verbose_name='F.Promesa', help_text="Fecha de promesa")
    ejecutivo = models.CharField(verbose_name='Ejecutivo', max_length=50, blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    uf_por_m2 = models.FloatField(verbose_name='UF Por M2', blank=True, null=True)
    motivo_compra = models.TextField(verbose_name='Motivo Compra', blank=True, null=True)
    atributos = models.TextField(verbose_name='Atributos', blank=True, null=True)
    ggoo = models.IntegerField(verbose_name='GGOO', help_text="Gastos Operacionales", blank=True, null=True)

    class Meta:
        db_table = 'venta'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        # unique_together = (('partida', 'id'),)
        ordering = ['id_venta']

    def __str__(self):
        return str(self.id_venta) + " - " + str(self.id_propiedad.numero_propiedad)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tipo_venta_original = self.tipo_venta

    def save(self, *args, **kwargs):
        propiedad = self.id_propiedad
        valor_inicial = propiedad.valor_inicial_propiedad or 0
        descuento = self.uf_descuento_campagna or 0
        bono = self.bono_pie or 0

        valor_final = valor_inicial - descuento - bono
        propiedad.valor_final_propiedad = valor_final

        if propiedad.metros_total_propiedad:
            self.uf_por_m2 = round(valor_final / propiedad.metros_total_propiedad, 2)
        else:
            self.uf_por_m2 = None

        self.precio_venta = valor_final
        propiedad.save()

        es_nueva = self._state.adding
        super().save(*args, **kwargs)

        if es_nueva:
            etapas = Etapas.objects.filter(tipo_venta_asociado=self.tipo_venta)
            for etapa in etapas:
                VentaEtapa.objects.create(id_venta=self, id_etapa=etapa)

        elif self.tipo_venta != self._tipo_venta_original:
            self.ventaetapa_set.all().delete()
            nuevas_etapas = Etapas.objects.filter(tipo_venta_asociado=self.tipo_venta)
            for etapa in nuevas_etapas:
                VentaEtapa.objects.create(id_venta=self, id_etapa=etapa)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self._state.adding and not Etapas.objects.filter(tipo_venta_asociado=self.tipo_venta).exists():
            raise ValidationError(f"No hay etapas configuradas para el tipo de venta: {self.tipo_venta}")


class Etapas(models.Model):
    id_etapa = models.AutoField(primary_key=True)
    nombre_etapa = models.CharField(verbose_name='Nombre Etapa', max_length=50, blank=True, null=True)
    alias_etapa = models.CharField(verbose_name='Alias Etapa', max_length=50, blank=True, null=True)
    tipo_venta_asociado = models.CharField(
        verbose_name='Tipo de Venta',
        choices=TIPO_VENTA_CHOICES,
        max_length=50,
        null=True, blank=True,
        help_text="Tipo de venta al que pertenece esta etapa"
    )
    descripcion_etapa = models.TextField(verbose_name='Descripcion Etapa', blank=True, null=True)

    class Meta:
        db_table = 'etapas'
        verbose_name = 'Etapa'
        verbose_name_plural = 'Etapas'
        # unique_together = (('partida', 'id'),)
        ordering = ['id_etapa']

    def __str__(self):
        return str(self.id_etapa) + " - " + str(self.alias_etapa)


class VentaEtapa(models.Model):
    id_venta_etapa = models.AutoField(primary_key=True)
    id_etapa = models.ForeignKey(Etapas, on_delete=models.CASCADE)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio', blank=True, null=True)
    fecha_fin = models.DateField(verbose_name='Fecha de Fin', blank=True, null=True)

    class Meta:
        db_table = 'venta_etapas'
        verbose_name = 'Venta Etapa'
        verbose_name_plural = 'Ventas Etapas'
        # unique_together = (('partida', 'id'),)
        ordering = ['id_venta_etapa']

    def __str__(self):
        return str(self.id_venta_etapa)


class CampoEtapa(models.Model):
    id_campo_etapa = models.AutoField(primary_key=True)
    id_etapa = models.ForeignKey(Etapas, on_delete=models.CASCADE)
    nombre_campo = models.CharField(verbose_name='Nombre Campo', max_length=50, blank=True, null=True)
    tipo_dato = models.CharField(
    max_length=20,
    choices=TIPO_DATO_CHOICES,
    default="Texto",
    verbose_name="Tipo de dato",
)
    obligatorio = models.BooleanField(verbose_name='Obligatorio', default=False)
    descripcion_campo = models.TextField(verbose_name='Descripcion Campo', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'campo_etapas'
        verbose_name = 'Campo Etapa'
        verbose_name_plural = 'Campos Etapas'
        ordering = ['id_etapa']
        # unique_together = (('id_etapa', 'nombre_campo'),)

    def __str__(self):
        return str(self.id_campo_etapa) + " - " + str(self.nombre_campo)


class ValoresEtapa(models.Model):
    id_valores_etapa = models.AutoField(primary_key=True)
    id_venta_etapa = models.ForeignKey(VentaEtapa, on_delete=models.CASCADE)
    id_campo_etapa = models.ForeignKey(CampoEtapa, on_delete=models.CASCADE)
    valor_campo = models.TextField(
    blank=True,
    null=True,
    verbose_name="Valor"
)

    class Meta:
        db_table = 'valores_etapas'
        verbose_name = 'Valor Etapa'
        verbose_name_plural = 'Valores Etapas'
        ordering = ['id_valores_etapa']

    def __str__(self):
        return str(self.id_valores_etapa)
