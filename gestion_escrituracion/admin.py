from django.contrib import admin, messages
from django.utils.html import format_html
from gestion_contable.admin import PagosInline  # Si mantienes Pagos relacionados a Venta
from utils_project.filters import CondominioFilter
from unfold.admin import ModelAdmin, TabularInline
from .models import Venta, Etapas, VentaEtapa, CampoEtapa, ValoresEtapa


# Valores de los campos asociados a una VentaEtapa
class ValoresEtapaInline(TabularInline):
    model = ValoresEtapa
    extra = 1


@admin.register(VentaEtapa)
# class VentaEtapaAdmin(admin.ModelAdmin):
class VentaEtapaAdmin(ModelAdmin):
    list_display = ('id_venta_etapa', 'id_venta', 'id_etapa', 'fecha_inicio', 'fecha_fin')
    list_filter = ('id_etapa',)
    date_hierarchy = 'fecha_inicio'
    ordering = ('fecha_inicio',)
    inlines = [ValoresEtapaInline]


# Campos que componen una Etapa
class CampoEtapaInline(TabularInline):
    model = CampoEtapa
    extra = 1


@admin.register(Etapas)
# class EtapasAdmin(admin.ModelAdmin):
class EtapasAdmin(ModelAdmin):
    list_display = ('id_etapa', 'tipo_venta_asociado','alias_etapa', 'nombre_etapa')
    search_fields = ('nombre_etapa', 'alias_etapa')
    ordering = ('id_etapa',)
    inlines = [CampoEtapaInline]


# Etapas asociadas a una Venta
class VentaEtapaInline(TabularInline):
    model = VentaEtapa
    extra = 0


@admin.register(Venta)
class VentaAdmin(ModelAdmin):
    # =========================================================
    # LISTADO DE VENTAS
    # =========================================================
    list_display = (
        "id_venta",
        "get_condominio",
        "get_etapa",
        "get_numero_propiedad",
        "id_cliente",
        "tipo_venta",
        "estado_venta",
        "fecha_venta",
        "fecha_promesa",
        "format_pventa",
        "ejecutivo",
    )

    list_display_links = (
        "id_venta",
        "get_numero_propiedad",
    )

    list_filter = (
        "fecha_venta",
        "estado_venta",
        "ejecutivo",
        "tipo_venta",
        CondominioFilter,
    )

    search_fields = (
        "id_propiedad__numero_propiedad",
        "id_propiedad__rol",
        "id_cliente__rut_cliente",
        "id_cliente__nombres_1",
        "id_cliente__nombres_2",
        "id_cliente__apellidos_1",
        "id_cliente__apellidos_2",
        "ejecutivo",
    )

    ordering = ("-fecha_venta",)
    date_hierarchy = "fecha_venta"
    list_per_page = 25

    list_select_related = (
        "id_propiedad",
        "id_propiedad__condominio",
        "id_propiedad__etapa",
        "id_cliente",
    )

    # =========================================================
    # FORMULARIO
    # =========================================================
    readonly_fields = (
        "precio_venta",
        "uf_por_m2",
    )
    fieldsets = (
        (
            "Información de la venta",
            {
                "fields": (
                    ("id_propiedad", "id_cliente"),
                    ("tipo_venta", "estado_venta"),
                    ("fecha_promesa", "ejecutivo"),
                ),
            },
        ),
        (
            "Descuentos y bonos",
            {
                "fields": (
                    ("descuento_campagna", "uf_descuento_campagna"),
                    ("bono_pie", "aplicacion_bono"),
                ),
            },
        ),
        (
            "Financiamiento",
            {
                "fields": (
                    ("credito_hipotecario", "saldo_contado"),
                    ("recursos_propio", "subsidio"),
                ),
            },
        ),
        (
            "Valores de la venta",
            {
                "fields": (
                    ("precio_venta", "uf_por_m2"),
                    "ggoo",
                ),
            },
        ),
        (
            "Información comercial",
            {
                "fields": (
                    "motivo_compra",
                    "atributos",
                ),
            },
        ),
    )

    inlines = [
        VentaEtapaInline,
        PagosInline,
    ]

    # =========================================================
    # COLUMNAS CALCULADAS
    # =========================================================
    @admin.display(
        description="Condominio",
        ordering="id_propiedad__condominio__alias_condominio",
    )
    def get_condominio(self, obj):
        return obj.id_propiedad.condominio.alias_condominio

    @admin.display(
        description="Etapa",
        ordering="id_propiedad__etapa__nombre_etapa",
    )
    def get_etapa(self, obj):
        return obj.id_propiedad.etapa.nombre_etapa

    @admin.display(
        description="N°",
        ordering="id_propiedad__numero_propiedad",
    )
    def get_numero_propiedad(self, obj):
        return obj.id_propiedad.numero_propiedad

    @admin.display(
        description="P. Inicial",
        ordering="id_propiedad__valor_inicial_propiedad",
    )
    def get_precio_ini_propiedad(self, obj):
        if obj.id_propiedad.valor_inicial_propiedad is None:
            return "-"

        return f"UF {obj.id_propiedad.valor_inicial_propiedad:,.0f}".replace(",", ".")

    @admin.display(
        description="GGOO",
        ordering="ggoo",
    )
    def format_ggoo(self, obj):
        if obj.ggoo is None:
            return "-"

        return f"$ {obj.ggoo:,.0f}".replace(",", ".")

    @admin.display(
        description="Dcto. Campaña",
        ordering="uf_descuento_campagna",
    )
    def format_ufdsctocam(self, obj):
        if obj.uf_descuento_campagna is None:
            return "-"

        return f"UF {obj.uf_descuento_campagna:,.0f}".replace(",", ".")

    @admin.display(
        description="P. Venta",
        ordering="precio_venta",
    )
    def format_pventa(self, obj):
        if obj.precio_venta is None:
            return "-"

        return f"UF {obj.precio_venta:,.0f}".replace(",", ".")

    # =========================================================
    # MENSAJES AL GUARDAR
    # =========================================================
    def save_model(self, request, obj, form, change):
        tipo_venta_anterior = None

        if change:
            old_obj = Venta.objects.get(pk=obj.pk)
            tipo_venta_anterior = old_obj.tipo_venta

        super().save_model(request, obj, form, change)

        if change and tipo_venta_anterior != obj.tipo_venta:
            self.message_user(
                request,
                (
                    "Las etapas fueron actualizadas automáticamente "
                    f"por cambio en tipo de venta a: {obj.tipo_venta}"
                ),
                level=messages.INFO,
            )

        elif not change:
            self.message_user(
                request,
                "La venta fue registrada exitosamente con sus etapas "
                "asignadas automáticamente.",
                level=messages.SUCCESS,
            )