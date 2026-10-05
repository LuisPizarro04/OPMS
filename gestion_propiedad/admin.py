from django.contrib import admin
from django.utils.html import format_html

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.forms import (
    ImportForm,
    SelectableFieldsExportForm,
)

from .models import (
    Condominio,
    Etapa,
    SubEtapa,
    Torre,
    Modelo,
    Propiedade,
)


# ============================================================
# CONDOMINIOS
# ============================================================

class EtapaInline(TabularInline):
    model = Etapa
    extra = 0
    fields = (
        "nombre_etapa",
    )


@admin.register(Condominio)
class CondominioAdmin(ModelAdmin):

    list_display = (
        "id_condominio",
        "nombre_condominio",
        "alias_condominio",
        "empresa_vende",
        "estado_condominio",
        "fecha_venta_condominio",
    )

    search_fields = (
        "nombre_condominio",
        "alias_condominio",
        "direccion_proyecto",
        "empresa_vende__razon_social",
        "empresa_vende__rut_empresa",
    )

    list_filter = (
        "estado_condominio",
        "empresa_vende",
    )

    ordering = (
        "-id_condominio",
    )

    list_select_related = (
        "empresa_vende",
    )

    inlines = [
        EtapaInline,
    ]

    fieldsets = (
        (
            "Información del proyecto",
            {
                "fields": (
                    ("nombre_condominio", "alias_condominio"),
                    "direccion_proyecto",
                ),
            },
        ),
        (
            "Información comercial",
            {
                "fields": (
                    ("empresa_vende", "estado_condominio"),
                    "fecha_venta_condominio",
                ),
            },
        ),
    )

# ============================================================
# ETAPAS
# ============================================================

class SubEtapaInline(TabularInline):
    model = SubEtapa
    extra = 0
    fields = (
        "nombre_sub_etapa",
    )


class TorreInline(TabularInline):
    model = Torre
    extra = 0

    fields = (
        "nombre_torre",
        "estado_torre",
    )


@admin.register(Etapa)
class EtapaAdmin(ModelAdmin):

    list_display = (
        "id_etapa_condominio",
        "nombre_etapa",
        "id_condominio",
    )

    search_fields = (
        "nombre_etapa",
        "id_condominio__nombre_condominio",
        "id_condominio__alias_condominio",
    )

    list_filter = (
        "id_condominio",
    )

    ordering = (
        "id_etapa_condominio",
    )

    list_select_related = (
        "id_condominio",
    )

    inlines = [
        SubEtapaInline,
        TorreInline,
    ]

    fieldsets = (
        (
            "Información de la etapa",
            {
                "fields": (
                    ("id_condominio", "nombre_etapa"),
                ),
            },
        ),
    )


# ============================================================
# SUB ETAPAS
# ============================================================

@admin.register(SubEtapa)
class SubEtapaAdmin(ModelAdmin):

    list_display = (
        "id_sub_etapa",
        "nombre_sub_etapa",
        "etapa",
    )

    search_fields = (
        "nombre_sub_etapa",
        "etapa__nombre_etapa",
        "etapa__id_condominio__nombre_condominio",
    )

    list_filter = (
        "etapa__id_condominio",
        "etapa",
    )

    ordering = (
        "id_sub_etapa",
    )

    list_select_related = (
        "etapa",
        "etapa__id_condominio",
    )


# ============================================================
# TORRES
# ============================================================

@admin.register(Torre)
class TorreAdmin(ModelAdmin):

    list_display = (
        "id_torre",
        "nombre_torre",
        "id_etapa_condominio",
        "estado_torre",
    )

    search_fields = (
        "nombre_torre",
        "id_etapa_condominio__nombre_etapa",
        "id_etapa_condominio__id_condominio__nombre_condominio",
    )

    list_filter = (
        "estado_torre",
        "id_etapa_condominio__id_condominio",
        "id_etapa_condominio",
    )

    ordering = (
        "id_torre",
    )

    list_select_related = (
        "id_etapa_condominio",
        "id_etapa_condominio__id_condominio",
    )

    fieldsets = (
        (
            "Información de la torre",
            {
                "fields": (
                    ("id_etapa_condominio", "nombre_torre"),
                    "estado_torre",
                ),
            },
        ),
    )


# ============================================================
# MODELOS
# ============================================================

@admin.register(Modelo)
class ModeloAdmin(ModelAdmin):

    list_display = (
        "id_modelo",
        "nombre_modelo",
        "programa_modelo",
        "estado_modelo",
    )

    search_fields = (
        "nombre_modelo",
        "programa_modelo",
    )

    list_filter = (
        "estado_modelo",
    )

    ordering = (
        "nombre_modelo",
    )

    fieldsets = (
        (
            "Información del modelo",
            {
                "fields": (
                    ("nombre_modelo", "programa_modelo"),
                    "estado_modelo",
                ),
            },
        ),
    )


# ============================================================
# IMPORT / EXPORT PROPIEDADES
# ============================================================

class PropiedadeResource(resources.ModelResource):

    class Meta:
        model = Propiedade

        skip_unchanged = True
        report_skipped = True

        import_id_fields = (
            "id_propiedad",
        )

        fields = (
            "id_propiedad",
            "numero_propiedad",
            "condominio",
            "etapa",
            "torre",
            "rol",
            "modelo",
            "estado_propiedad",
            "ori_propiedad",
            "piso",
            "metros_vivienda",
            "metros_terraza_propiedad",
            "metros_total_propiedad",
            "bono_propiedad",
            "prorrateo_propiedad",
            "estacionamiento",
            "valor_estacionamiento",
            "rol_estacionamiento",
            "bodega",
            "valor_bodega",
            "rol_bodega",
            "m2_bodega",
            "valor_inicial_propiedad",
            "valor_final_propiedad",
            "valor_cchc",
            "fpm",
        )


# ============================================================
# PROPIEDADES
# ============================================================

@admin.register(Propiedade)
class PropiedadeAdmin(ModelAdmin, ImportExportModelAdmin):

    resource_class = PropiedadeResource

    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm

    # --------------------------------------------------------
    # LISTADO
    # --------------------------------------------------------

    list_display = (
        "numero_propiedad",
        "condominio",
        "etapa",
        "torre",
        "modelo",
        "piso",
        "ori_propiedad",
        "estado_propiedad",
        "format_vfp",
    )

    list_display_links = (
        "numero_propiedad",
    )

    # --------------------------------------------------------
    # BÚSQUEDA
    # --------------------------------------------------------

    search_fields = (
        "numero_propiedad",
        "rol",
        "condominio__nombre_condominio",
        "condominio__alias_condominio",
        "etapa__nombre_etapa",
        "torre__nombre_torre",
        "modelo__nombre_modelo",
    )

    # --------------------------------------------------------
    # FILTROS
    # --------------------------------------------------------

    list_filter = (
        "estado_propiedad",
        "condominio",
        "etapa",
        "torre",
        "modelo",
        "piso",
        "ori_propiedad",
    )

    ordering = (
        "-id_propiedad",
    )

    list_select_related = (
        "condominio",
        "etapa",
        "torre",
        "modelo",
    )

    list_per_page = 30

    # --------------------------------------------------------
    # FORMULARIO
    # --------------------------------------------------------

    fieldsets = (
        (
            "Ubicación de la propiedad",
            {
                "fields": (
                    ("condominio", "etapa"),
                    ("torre", "numero_propiedad"),
                    ("piso", "ori_propiedad"),
                    "rol",
                ),
            },
        ),
        (
            "Características",
            {
                "fields": (
                    ("modelo", "estado_propiedad"),
                    (
                        "metros_vivienda",
                        "metros_terraza_propiedad",
                        "metros_total_propiedad",
                    ),
                    ("bono_propiedad", "prorrateo_propiedad"),
                ),
            },
        ),
        (
            "Estacionamiento",
            {
                "fields": (
                    ("estacionamiento", "rol_estacionamiento"),
                    "valor_estacionamiento",
                ),
            },
        ),
        (
            "Bodega",
            {
                "fields": (
                    ("bodega", "rol_bodega"),
                    ("m2_bodega", "valor_bodega"),
                ),
            },
        ),
        (
            "Valores comerciales",
            {
                "fields": (
                    ("valor_inicial_propiedad", "valor_final_propiedad"),
                    ("valor_cchc", "fpm"),
                ),
            },
        ),
    )

    # --------------------------------------------------------
    # FORMATO PRECIOS
    # --------------------------------------------------------

    @admin.display(
        description="Precio final",
        ordering="valor_final_propiedad",
    )
    def format_vfp(self, obj):
        if obj.valor_final_propiedad is None:
            return "-"

        return f"UF {obj.valor_final_propiedad:,.0f}".replace(",", ".")

    @admin.display(
        description="Precio inicial",
        ordering="valor_inicial_propiedad",
    )
    def format_vip(self, obj):
        if obj.valor_inicial_propiedad is None:
            return "-"

        return f"UF {obj.valor_inicial_propiedad:,.0f}".replace(",", ".")