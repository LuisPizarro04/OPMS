from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    RequerimientoPostVenta,
    Recinto,
    Lugar,
    Item,
    Problema,
    Especialidad,
    Causa,
    AlcanceResponsabilidad,
)


# ============================================================
# CATÁLOGOS DE POSTVENTA
# ============================================================

@admin.register(Recinto)
class RecintoAdmin(ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)
    ordering = ("nombre",)
    list_per_page = 25


@admin.register(Lugar)
class LugarAdmin(ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)
    ordering = ("nombre",)
    list_per_page = 25


@admin.register(Item)
class ItemAdmin(ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)
    ordering = ("nombre",)
    list_per_page = 25


@admin.register(Problema)
class ProblemaAdmin(ModelAdmin):
    list_display = ("descripcion",)
    search_fields = ("descripcion",)
    ordering = ("descripcion",)
    list_per_page = 25


@admin.register(Especialidad)
class EspecialidadAdmin(ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)
    ordering = ("nombre",)
    list_per_page = 25


@admin.register(Causa)
class CausaAdmin(ModelAdmin):
    list_display = ("descripcion",)
    search_fields = ("descripcion",)
    ordering = ("descripcion",)
    list_per_page = 25


@admin.register(AlcanceResponsabilidad)
class AlcanceResponsabilidadAdmin(ModelAdmin):
    list_display = ("descripcion",)
    search_fields = ("descripcion",)
    ordering = ("descripcion",)
    list_per_page = 25


# ============================================================
# REQUERIMIENTOS DE POSTVENTA
# ============================================================

@admin.register(RequerimientoPostVenta)
class RequerimientoPostVentaAdmin(ModelAdmin):

    list_display = (
        "fecha",
        "get_proyecto",
        "get_numero_depto",
        "get_piso",
        "recinto",
        "item",
        "especialidad",
        "estado",
        "format_total",
    )

    list_display_links = (
        "fecha",
        "get_numero_depto",
    )

    list_filter = (
        "estado",
        "especialidad",
        "recinto",
        "propiedad__condominio",
        "propiedad__etapa",
        "fecha",
    )

    search_fields = (
        "propiedad__numero_propiedad",
        "propiedad__condominio__alias_condominio",
        "recinto__nombre",
        "lugar__nombre",
        "item__nombre",
        "problema__descripcion",
        "especialidad__nombre",
        "causa__descripcion",
        "solicitud_cliente",
        "comentario",
    )

    ordering = (
        "-fecha",
    )

    date_hierarchy = "fecha"

    list_per_page = 25

    list_select_related = (
        "propiedad",
        "propiedad__condominio",
        "propiedad__etapa",
        "recinto",
        "lugar",
        "item",
        "problema",
        "especialidad",
        "causa",
        "alcance_responsabilidad",
    )

    readonly_fields = (
        "total",
    )

    fieldsets = (
        (
            "Propiedad y solicitud",
            {
                "fields": (
                    ("fecha", "propiedad"),
                    "solicitud_cliente",
                ),
            },
        ),
        (
            "Clasificación del requerimiento",
            {
                "fields": (
                    ("recinto", "lugar"),
                    ("item", "problema"),
                    ("especialidad", "causa"),
                    "alcance_responsabilidad",
                ),
            },
        ),
        (
            "Estado",
            {
                "fields": (
                    "estado",
                ),
            },
        ),
        (
            "Costos",
            {
                "fields": (
                    ("mo", "materiales"),
                    ("subcontrato", "total"),
                ),
                "description": (
                    "El costo total se calcula automáticamente a partir "
                    "de mano de obra, materiales y subcontrato."
                ),
            },
        ),
        (
            "Observaciones",
            {
                "fields": (
                    "comentario",
                ),
            },
        ),
    )

    @admin.display(
        description="Proyecto",
        ordering="propiedad__condominio__alias_condominio",
    )
    def get_proyecto(self, obj):
        return obj.propiedad.condominio.alias_condominio

    @admin.display(
        description="Depto",
        ordering="propiedad__numero_propiedad",
    )
    def get_numero_depto(self, obj):
        return obj.propiedad.numero_propiedad

    @admin.display(
        description="Piso",
        ordering="propiedad__piso",
    )
    def get_piso(self, obj):
        return obj.propiedad.piso

    @admin.display(
        description="Total",
        ordering="total",
    )
    def format_total(self, obj):
        if obj.total is None:
            return "-"

        return f"${obj.total:,.0f}".replace(",", ".")